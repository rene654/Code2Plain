# Code2Plain Companion — iOS

Minimal iPhone companion for Code2Plain.

Responsibilities:

- request notification authorization
- register with APNs
- receive the current APNs device token
- pair with a Code2Plain learner/device
- securely forward the APNs token to the backend
- receive learning digest notifications

This companion is intentionally not:

- a code editor
- a chatbot
- a course application
- a second Code2Plain desktop interface

The learning engine remains on the Code2Plain backend/desktop side.

## Build requirement

The iOS project must ultimately be created/opened in Xcode on macOS.

Required Apple capability:

- Push Notifications

Bundle identifier placeholder:

com.code2plain.app

Replace it with the final registered App ID before real APNs testing.
