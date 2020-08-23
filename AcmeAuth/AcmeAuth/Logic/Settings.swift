// AcmeAuth/Settings.swift
// 


import Foundation

struct ConnectorSettings {
    var host: String = "konnektor.local"
    var username: String?
    var password: String?
    var x509Cert: String?
    var mandantId: String = "CompanionApp"
    var clientSystemId: String = "CompanionApp"
    var workSPaceId: String = "CompanionApp"
}

class AppSettings: ObservableObject {
    @Published var connector = ConnectorSettings()
    @Published var apiBaseURL = URL(string: "https://appauth.acme.spilikin.dev/api/")!
    @Published var acct: String {
         didSet {
             UserDefaults.standard.set(acct, forKey: "acct")
         }
     }

    @Published var isEnrolled: Bool {
         didSet {
             UserDefaults.standard.set(isEnrolled, forKey: "isEnrolled")
         }
     }

    init() {
        self.acct = UserDefaults.standard.object(forKey: "acct") as?
            String ?? "\(Int.random(in: 0...10000000))@healthid.life"
        self.isEnrolled = UserDefaults.standard.bool(forKey: "isEnrolled")

    }
    
    func apiURL(for resource: String, params: [String: String] = [:]) -> URL {
        var builder = URLComponents(string: URL(string: resource, relativeTo: apiBaseURL)!.absoluteURL.description )!
        if !params.isEmpty {
            builder.queryItems = params.map { (k,v) in
                URLQueryItem(name: k, value: v)
            }
        }
        return builder.url!
    }
    
    func reset() {
        self.isEnrolled = false
    }
}
