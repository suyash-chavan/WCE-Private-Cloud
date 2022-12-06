package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"sync"

	"github.com/gliderlabs/ssh"
	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func initEnv() {
	err := godotenv.Load(".env")

	if err != nil {
		log.Fatalf("Error loading .env file")
	}
}

func getEnv(key string) string {
	return os.Getenv(key)
}

var mongoClient *mongo.Client

// GetMongoClient - Return mongodb connection to work with
func getMongoClient(MONGO_URI string) (*mongo.Client, error) {

	/* Used to create a singleton object of MongoDB client.
	Initialized and exposed through  GetMongoClient().*/
	var clientInstance *mongo.Client

	//Used during creation of singleton client object in GetMongoClient().
	var clientInstanceError error

	//Used to execute client creation procedure only once.
	var mongoOnce sync.Once

	//Perform connection creation operation only once.
	mongoOnce.Do(func() {
		// Set client options
		clientOptions := options.Client().ApplyURI(MONGO_URI)
		// Connect to MongoDB
		client, err := mongo.Connect(context.TODO(), clientOptions)
		if err != nil {
			clientInstanceError = err
		}
		// Check the connection
		err = client.Ping(context.TODO(), nil)
		if err != nil {
			clientInstanceError = err
		}
		clientInstance = client
	})

	return clientInstance, clientInstanceError
}

func initDatabase() {

	clientInstance, err := getMongoClient(getEnv("MONGO_URI"))

	if err != nil {
		log.Fatal(err)
	}

	err = clientInstance.Ping(context.TODO(), nil)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to MongoDB!")

	mongoClient = clientInstance
}

func main() {

	initEnv()
	initDatabase()

	ssh.Handle(func(s ssh.Session) {

		instanceName := s.User()

		instance := mongoClient.Database("wce-private-cloud").Collection("instance").FindOne(context.TODO(), map[string]string{
			"instanceName": instanceName,
		})

		if instance.Err() != nil {
			io.WriteString(s, fmt.Sprintf("Invalid instance name: %s", instanceName))
			s.Exit(1)
		}

		type structInstance struct {
			InstanceName string `bson:"instanceName"`
			InstanceType string `bson:"instanceType"`
			InstanceRam  int64  `bson:"instanceRam"`
			InstanceIp   string `bson:"instanceIp"`
		}

		var instanceData structInstance

		err := instance.Decode(&instanceData)

		if err != nil {
			io.WriteString(s, fmt.Sprintf("Error decoding instance data: %s", err))
			s.Exit(1)
		}

		fmt.Println(instanceData.InstanceIp)

		io.WriteString(s, fmt.Sprintf("Hello %s\n", s.User()))
	})

	log.Println("starting ssh server on port 2222...")
	log.Fatal(ssh.ListenAndServe(":2222", nil))
}
