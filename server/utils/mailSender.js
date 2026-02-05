const nodemailer = require("nodemailer")

const mailSender = async (email, title, body) => {
  try {
    let transporter = nodemailer.createTransport({
      host: process.env.MAIL_HOST,      // smtp.gmail.com
      port: 587,                        // ✅ VERY IMPORTANT
      secure: false,                    // must be false for 587
      auth: {
        user: process.env.MAIL_USER,    // your gmail
        pass: process.env.MAIL_PASS,    // GOOGLE APP PASSWORD
      },
    })

    let info = await transporter.sendMail({
      from: `"Techvidya" <${process.env.MAIL_USER}>`,
      to: email,
      subject: title,
      html: body,
    })

    console.log("✅ Email sent:", info.messageId)
    return info

  } catch (error) {
    console.error("❌ Email Error:", error)
    throw error
  }
}

module.exports = mailSender
