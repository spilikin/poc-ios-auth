import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var appState: AppState
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        Form {
            accountSection
            connectorSection
            Section {
                Button(action: {
                    appState.settings.reset()
                    // TODO: mage bette state change
                    appState.debugLog = ""
                    presentationMode.wrappedValue.dismiss()
                }) {
                    Text("Reset All Settings")
                        .foregroundColor(Color.red)
                }
            }
        }
        .navigationBarTitle(Text("Settings"))
    }

    var accountSection: some View {
        Section(header: Text("ACCOUNT")) {
            TextField("Account", text: $appState.settings.acct).disabled(true)
        }
    }

    var connectorSection: some View {
    Section(header: Text("CONNECTOR")) {
        VStack(alignment: .leading) {
            Text("Host").font(.headline)
            TextField("Username", text: $appState.settings.connector.host)
            Text("Mandant ID").font(.headline)
            TextField("Mandant ID", text: $appState.settings.connector.mandantId)
            Text("Clientsystem ID").font(.headline)
            TextField("Clientsystem ID", text: $appState.settings.connector.clientSystemId)
            Text("Workplace ID").font(.headline)
            TextField("Workplace ID", text: $appState.settings.connector.clientSystemId)
        }
    }

    }
}

