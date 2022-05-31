const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');

const userSchema = new mongoose.Schema({
    prn: {
        type: String,
        required: true,
        unique: true
    },
    google: {
        mailId: {
            type: String,
            required: true,
            unique: true
        }
        , accessToken: {
            type: String,
            required: true,
            unique: true
        }
    },
    services: {
        compute: {
            instanceId: [{
                id: {
                    type: String,
                    unique: true
                }
            }],
            limit: {
                type: Number,
                required: true
            }
        },
        keypair: {
            
        }
    },
    banned: {
        type: Boolean,
        default: false
    }
});

userSchema.methods.generateAuthToken = function () {
    const { _id, prn} = this;
    const token = jwt.sign(
        { _id, prn},
        process.env.JWT_PRIVATE_KEY
    );
    return token;
};

