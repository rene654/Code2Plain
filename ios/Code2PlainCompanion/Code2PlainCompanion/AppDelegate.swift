import UIKit
import UserNotifications

final class AppDelegate: NSObject, UIApplicationDelegate {

    weak var appState: AppState?

    func application(
        _ application: UIApplication,
        didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
    ) {

        let token = deviceToken
            .map {
                String(
                    format: "%02x",
                    $0
                )
            }
            .joined()

        Task { @MainActor in
            self.appState?.updateAPNsToken(
                token
            )
        }
    }

    func application(
        _ application: UIApplication,
        didFailToRegisterForRemoteNotificationsWithError error: Error
    ) {

        Task { @MainActor in
            self.appState?.reportError(
                "APNs registration failed"
            )
        }
    }
}
