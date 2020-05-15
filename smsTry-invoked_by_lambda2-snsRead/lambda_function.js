const AWS = require('aws-sdk');
const SES = new AWS.SES({ region: 'ap-south-1' });

exports.handler = async (params)  => {
  console.log("This is params:  ",params);

  const {
    to,
    from,
    subject,
    replyTo
  } = params;
const fromBase64 = Buffer.from('Uday').toString('base64');
  const htmlBody = `
    <!DOCTYPE html>
    <html>
      <head></head>
      <body><h1>Amount Has been credited to your account</h1></body>
    </html>
  `;

  const sesParams = {
    Destination: {
      ToAddresses: [to],
    },
    Message: {
      Body: {
        Html: {
          Charset: 'UTF-8',
          Data: htmlBody,
        },
      },
      Subject: {
        Charset: 'UTF-8',
        Data: subject,
      },
    },
    //ReplyToAddresses: [replyTo],
    Source: `=?utf-8?B?${fromBase64}?= <udaysrivastava0@gmail.com>`,
  };

  const response = await SES.sendEmail(sesParams).promise();

  console.log(response);
};