import SwiftUI

struct ContentView: View {

    @ObservedObject var appState: AppState

    let apiClient: APIClient

    private let bundleId = "com.code2plain.app"

    var body: some View {

        NavigationStack {

            VStack(
                spacing: 24
            ) {

                Image(
                    systemName:
                        "brain.head.profile"
                )
                .font(
                    .system(
                        size: 64
                    )
                )

                Text(
                    "Code2Plain"
                )
                .font(
                    .largeTitle
                    .bold()
                )

                Text(
                    "Learning Companion"
                )
                .foregroundStyle(
                    .secondary
                )

                TextField(
                    "Pairing token",
                    text:
                        $appState.pairingToken
                )
                .textInputAutocapitalization(
                    .never
                )
                .autocorrectionDisabled()
                .textFieldStyle(
                    .roundedBorder
                )

                Button(
                    "Connect iPhone"
                ) {
                    Task {
                        await connect()
                    }
                }
                .buttonStyle(
                    .borderedProminent
                )

                Divider()

                HStack {

                    Image(
                        systemName:
                            appState.isPaired
                            ? "checkmark.circle.fill"
                            : "circle"
                    )

                    Text(
                        appState.statusText
                    )
                }

                Spacer()
            }
            .padding()
        }
    }


    @MainActor
    private func connect() async {

        let pairingToken = (
            appState
                .pairingToken
                .trimmingCharacters(
                    in:
                        .whitespacesAndNewlines
                )
        )

        guard !pairingToken.isEmpty else {
            appState.reportError(
                "Pairing token required"
            )

            return
        }

        do {

            try await NotificationManager
                .requestAndRegister()

            appState.statusText = (
                "Waiting for APNs token..."
            )

        } catch {

            appState.reportError(
                "Notification permission denied"
            )
        }
    }
}
