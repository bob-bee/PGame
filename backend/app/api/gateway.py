To build an ingress controller that handles cross-instance message routing and signature verification for ActivityPub, you can follow these steps:

1. Define the requirements:
   - Ingress Controller must be able to route messages between different instances.
   - Signature verification must ensure that incoming messages are authentic.

2. Choose a programming language and framework:
   - For this task, Python with Flask or Django would be a good choice.

3. Design the architecture:
   - Create separate endpoints for receiving and sending messages.
   - Implement signature verification logic to validate incoming messages.

4. Implement cross-instance message routing:
   - Use a database or in-memory storage to keep track of instance information.
   - When a message is received, determine which instance should receive it based on the sender's ID.
   - Route the message to the appropriate instance using a message queue or direct API calls.

5. Implement signature verification:
   - Extract the signature and signing key from the incoming message.
   - Use a library like PyJWT (for JWT signatures) or cryptography (for other types of signatures).
   - Verify the signature using the sender's public key.

6. Test your ingress controller:
   - Send messages between different instances to ensure that routing works as expected.
   - Simulate signature tampering and verify that it is caught by your implementation.

7. Deploy your ingress controller:
   - Choose a deployment strategy (e.g., Docker, Kubernetes).
   - Ensure that your ingress controller can handle high traffic volumes.

Remember to follow best practices for security and scalability when building your ingress controller.