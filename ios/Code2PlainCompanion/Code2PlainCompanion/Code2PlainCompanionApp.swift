import SwiftUI

@main
struct Code2PlainCompanionApp: App {

    @UIApplicationDelegateAdaptor(
        AppDelegate.self
    )
    private var appDelegate

    @StateObject
    private var appState =
        AppState()

    private let apiClient = APIClient(
        baseURL: URL(
            string:
                "https://replace-with-code2plain-backend.example"
        )!
    )

    init() {
    }

    var body: some Scene {

        WindowGroup {

            ContentView(
                appState:
                    appState,
                apiClient:
                    apiClient
            )
            .onAppear {

                appDelegate.appState =
                    appState
            }
        }
    }
}
