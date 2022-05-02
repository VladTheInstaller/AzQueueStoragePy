## pip install azure-storage-queue

from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)
import os, uuid
# Retrieve the connection string from an environment
# variable named AZURE_STORAGE_CONNECTION_STRING
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#connect_str = "<myConnectionString>"


# Create a unique name for the queue
#q_name = "queue-" + str(uuid.uuid4())

# use a static name for the queue
q_name = "vladqueue001"

# Instantiate a QueueClient object
#print("Creating queue: " + q_name)
queue_client = QueueClient.from_connection_string(connect_str, q_name)
# # Create the queue
# queue_client.create_queue()

# # Setup Base64 encoding and decoding functions (not currently using this)
# base64_queue_client = QueueClient.from_connection_string(
#                             conn_str=connect_str, queue_name=q_name,
#                             message_encode_policy = BinaryBase64EncodePolicy(),
#                             message_decode_policy = BinaryBase64DecodePolicy()
#                         )

message = u"Hello Reader. This is a message."
#message = 'whattsa matta U?'

print("Adding message: " + message)
queue_client.send_message(message)

# Peek at the first message
messages = queue_client.peek_messages()
for peeked_message in messages:
    print("Peeked message: " + peeked_message.content)

# modify the message
messages = queue_client.receive_messages()
list_result = next(messages)
message = queue_client.update_message(
        list_result.id, list_result.pop_receipt,
        visibility_timeout=0, content=u'I am replacing the old message.')
print("Updated message to: " + message.content)

# Dequeue the messages in the queue
messages = queue_client.receive_messages()
for message in messages:
    print("Dequeuing message: " + message.content)
    queue_client.delete_message(message.id, message.pop_receipt)

# Batch delete all messages in queue
# messages = queue_client.receive_messages(messages_per_page=5, visibility_timeout=5*60)
# for msg_batch in messages.by_page():
#    for msg in msg_batch:
#       print("Batch dequeue message: " + msg.content)
#       queue_client.delete_message(msg)

# Delete the queue
# print("Deleting queue: " + queue_client.queue_name)
# queue_client.delete_queue()