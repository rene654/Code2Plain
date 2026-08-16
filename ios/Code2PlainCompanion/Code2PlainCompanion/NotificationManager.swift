import UIKit
import UserNotifications

enum NotificationPermissionError: Error {
    case denied
}

struct NotificationManager {

    static func requestAndRegister() async throws {

        let center = UNUserNotificationCenter.current()

        let granted = try await center.requestAuthorization(
            options: [
                .alert,
                .sound,
                .badge
            ]
        )

        guard granted else {
            throw NotificationPermissionError.denied
        }

        await MainActor.run {
            UIApplication.shared
                .registerForRemoteNotifications()
        }
    }
}
