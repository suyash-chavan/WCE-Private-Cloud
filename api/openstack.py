import openstack
import openstack.config.loader
import openstack.compute.v2.server

# Initialize and turn on debug logging
openstack.enable_logging(debug=True)

# Initialize connection
conn = openstack.connect(cloud='openstack')