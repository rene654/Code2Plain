import Foundation

struct RegisterApplePushRequest: Codable {
    let pairingToken: String
    let apnsToken: String
    let bundleId: String
    let environment: String
}

struct RegisterApplePushResponse: Codable {
    let deviceId: String
    let status: String
}

enum APIClientError: Error {
    case invalidURL
    case invalidResponse
    case serverError(Int)
}

final class APIClient {
    private let baseURL: URL

    init(baseURL: URL) {
        self.baseURL = baseURL
    }

    func registerApplePush(
        pairingToken: String,
        apnsToken: String,
        bundleId: String,
        environment: String
    ) async throws -> RegisterApplePushResponse {

        let endpoint = baseURL
            .appendingPathComponent("api")
            .appendingPathComponent("v1")
            .appendingPathComponent("devices")
            .appendingPathComponent("apple")
            .appendingPathComponent("register")

        var request = URLRequest(url: endpoint)

        request.httpMethod = "POST"

        request.setValue(
            "application/json",
            forHTTPHeaderField: "Content-Type"
        )

        request.httpBody = try JSONEncoder().encode(
            RegisterApplePushRequest(
                pairingToken: pairingToken,
                apnsToken: apnsToken,
                bundleId: bundleId,
                environment: environment
            )
        )

        let (data, response) = try await URLSession.shared.data(
            for: request
        )

        guard let http = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        guard (200...299).contains(http.statusCode) else {
            throw APIClientError.serverError(
                http.statusCode
            )
        }

        return try JSONDecoder().decode(
            RegisterApplePushResponse.self,
            from: data
        )
    }
}
