from cf_utils import cf_utils

class MessageHubUtil:

  def __init__(self, target_endpoint, username, password, organization_name, space_name):
    self.cf = cf_utils.CloudFoundryUtil(target_endpoint, username, password, organization_name, space_name) 
   
  def create_topic(self, messagehub_instance_name, topic_name):
      import requests
      import json
      
      api_key = self.cf.get_service_credential(messagehub_instance_name, 'api_key')

      data = { 'name' : topic_name }
      headers = {
          'content-type': 'application/json',
          'X-Auth-Token' : api_key 
      }
      url = kafka_admin_url + '/admin/topics'

      # create the topic (http POST)
      response = requests.post(url, headers = headers, data = json.dumps(data))

      # verify the topic was created (http GET)
      response = requests.get(url, headers = headers, data = json.dumps(data))
      print (response.text)
   
  def produce_message(self, messagehub_instance_name, messagehub_topic_name, message):

    # FIXME:this is a lot of overhead - creating a new KafkaProducer each time
    # a message is produced

    bootstrap_servers = self.cf.get_service_credential(messagehub_instance_name, 'kafka_brokers_sasl')
    sasl_plain_username = self.cf.get_service_credential(messagehub_instance_name, 'user')
    sasl_plain_password = self.cf.get_service_credential(messagehub_instance_name, 'password')
    api_key = self.cf.get_service_credential(messagehub_instance_name, 'api_key')
    kafka_admin_url = self.cf.get_service_credential(messagehub_instance_name, 'kafka_admin_url')
    kafka_rest_url = self.cf.get_service_credential(messagehub_instance_name, 'kafka_rest_url')

    from kafka import KafkaProducer
    from kafka.errors import KafkaError
    import ssl

    sasl_mechanism = 'PLAIN'
    security_protocol = 'SASL_SSL'

    # Create a new context using system defaults, disable all but TLS1.2
    context = ssl.create_default_context()
    context.options &= ssl.OP_NO_TLSv1
    context.options &= ssl.OP_NO_TLSv1_1

    producer = KafkaProducer(bootstrap_servers = bootstrap_servers,
                             sasl_plain_username = sasl_plain_username,
                             sasl_plain_password = sasl_plain_password,
                             security_protocol = security_protocol,
                             ssl_context = context,
                             sasl_mechanism = sasl_mechanism,
                             api_version = (0,10))

    producer.send(messagehub_topic_name, message)
    producer.flush()
    
  def consume_messages(self, messagehub_instance_name, messagehub_topic_name):
  
    bootstrap_servers = self.cf.get_service_credential(messagehub_instance_name, 'kafka_brokers_sasl')
    sasl_plain_username = self.cf.get_service_credential(messagehub_instance_name, 'user')
    sasl_plain_password = self.cf.get_service_credential(messagehub_instance_name, 'password')
    api_key = self.cf.get_service_credential(messagehub_instance_name, 'api_key')
    kafka_admin_url = self.cf.get_service_credential(messagehub_instance_name, 'kafka_admin_url')
    kafka_rest_url = self.cf.get_service_credential(messagehub_instance_name, 'kafka_rest_url')
    
    from kafka import KafkaConsumer
    from kafka.errors import KafkaError
    from uuid import uuid1
    import ssl

    sasl_mechanism = 'PLAIN'
    security_protocol = 'SASL_SSL'

    # Create a new context using system defaults, disable all but TLS1.2
    context = ssl.create_default_context()
    context.options &= ssl.OP_NO_TLSv1
    context.options &= ssl.OP_NO_TLSv1_1

    consumer = KafkaConsumer(topic_name,
                             bootstrap_servers = bootstrap_servers,
                             sasl_plain_username = sasl_plain_username,
                             sasl_plain_password = sasl_plain_password,
                             security_protocol = security_protocol,
                             ssl_context = context,
                             sasl_mechanism = sasl_mechanism,
                             api_version = (0,10),
                             consumer_timeout_ms = 10000,
                             auto_offset_reset = 'earliest',
                             group_id = uuid1() # consume all messages
                            )

    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                              message.offset, message.key,
                                              message.value))
                                              
  def get_properties(self, messagehub_instance_name):
  
    bootstrap_servers = self.cf.get_service_credential(messagehub_instance_name, 'kafka_brokers_sasl')
    sasl_plain_username = self.cf.get_service_credential(messagehub_instance_name, 'user')
    sasl_plain_password = self.cf.get_service_credential(messagehub_instance_name, 'password')
    api_key = self.cf.get_service_credential(messagehub_instance_name, 'api_key')
    kafka_admin_url = self.cf.get_service_credential(messagehub_instance_name, 'kafka_admin_url')
    kafka_rest_url = self.cf.get_service_credential(messagehub_instance_name, 'kafka_rest_url')
    
    return  + \
      'bootstrap_servers={0}\n'.format(','.join(bootstrap_servers)) + \
      'sasl_username={0}\n'.format(sasl_plain_username) + \
      'sasl_password={0}\n'.format(sasl_plain_password) + \
      'api_key={0}\n'.format(api_key) + \
      'kafka_admin_url={0}\n'.format(kafka_admin_url) + \
      'kafka_rest_url={0}\n'.format(kafka_rest_url)
