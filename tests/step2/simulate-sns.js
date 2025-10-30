// tests/step2/simulate-sns.js
// Simula un POST SNS Notification al bridge
const axios = require('axios');

const BRIDGE_URL = process.env.BRIDGE_URL || 'http://localhost:3000/sns';

async function main() {
  const snsNotification = {
    Type: 'Notification',
    MessageId: 'test-message-id',
    TopicArn: 'arn:aws:sns:us-east-1:123456789012:my-topic',
    Subject: 'Test SNS',
    Message: JSON.stringify({
      bucket: 'raw-snapshots',
      key: 'test-image.jpg',
      eventTime: new Date().toISOString()
    }),
    Timestamp: new Date().toISOString(),
    SignatureVersion: '1',
    Signature: 'test-signature',
    SigningCertURL: 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService.pem',
    UnsubscribeURL: 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe'
  };

  try {
    const res = await axios.post(BRIDGE_URL, snsNotification, {
      headers: {
        'x-amz-sns-message-type': 'Notification',
        'Content-Type': 'application/json'
      }
    });
    console.log('Respuesta del bridge:', res.status, res.data);
  } catch (err) {
    console.error('Error al enviar SNS simulado:', err.message);
    if (err.response) {
      console.error('Respuesta:', err.response.status, err.response.data);
    }
  }
}

main();
