import Foundation

@MainActor
final class AppState: ObservableObject {
    @Published var pairingToken: String = ""
    @Published var apnsToken: String?
    @Published var statusText: String = "Not connected"
    @Published var isPaired: Bool = false

    func updateAPNsToken(_ token: String) {
        apnsToken = token
        statusText = "APNs ready"
    }

    func markPaired() {
        isPaired = true
        statusText = "Connected"
    }

    func reportError(_ message: String) {
        statusText = message
    }
}
