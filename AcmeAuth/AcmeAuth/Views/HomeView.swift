import SwiftUI
import Combine

struct HomeView: View {
    @EnvironmentObject var appState: AppState
    
    func debug(_ text: String) {
        self.appState.debugLog = text + "\n" + self.appState.debugLog
    }
    
    @ViewBuilder var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .center) {
                    if (appState.settings.isEnrolled) {
                        accountButton
                        scannerButton
                        readCardButton
                        visitWebButton
                    } else {
                        enrollButton
                    }
                    debugView
                }
                .navigationBarTitle(Text("Acme Companion"))
                .navigationBarItems(trailing: settingsButton)
                .sheet(isPresented: $appState.isSpecialScreenState) {
                    sheetView()
                }
            }
        }

    }
        
    func sheetView() -> AnyView {
        switch appState.screenState {
        case .scanning:
            return AnyView(ScannerView(showSheetView: $appState.isSpecialScreenState))
        case .authenticating:
            return AnyView(AuthView(showSheetView: $appState.isSpecialScreenState, authRequest: appState.authRequest!))
        case .normal:
            return AnyView(Text(""))
        }
    }

    let nfc = NFCUtility()
    var readCardButton: some View {
        Button(action: {
            nfc.pollCardInfo {
                value in
                print(value)
            }
        }) {
            HStack(alignment: .center) {
                Image(systemName: "creditcard")
                    .font(.largeTitle)
                    .foregroundColor(.white)
                Text("Add Smartcard")
                Spacer()
            }.padding()
                .foregroundColor(.white)
                .background(Color.accentColor)
                .cornerRadius(15)
        }
        .padding()

    }

    var debugView: some View {
        Text(self.appState.debugLog)
            .font(Font.system(.footnote, design: .monospaced))
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
    }

    var accountButton: some View {
        VStack(alignment: .center) {

            Text(appState.settings.acct)
                .font(.title)
                .padding()

            Image(systemName: "checkmark.seal.fill")
                .resizable()
                .frame(width: 64, height: 64)
                .padding()
            HStack {
                Spacer()
            }
        }
        .foregroundColor(.white)
        .background(Color.green)
        .cornerRadius(20)
        .padding()
    }

    var enrollButton: some View {
        VStack(alignment: .leading) {

            Text("""
Enroll your identity at the Identity Provider and register this device as an autentication key
""")
                .padding()
                .lineLimit(3)

            NavigationLink(destination: EnrollmentView()) {
                HStack(alignment: .center) {
                    Image(systemName: "lock.shield.fill")
                        .font(.largeTitle)
                        .foregroundColor(.white)
                    Text("Start enrollment")
                    Spacer()
                    Image(systemName: "chevron.right")
                }
                .padding()
            }
        }
        .foregroundColor(.white)
        .background(Color.accentColor)
        .cornerRadius(20)
        .padding()
    }

    var scannerButton: some View {
        VStack(alignment: .leading) {
            Text("""
Using this feature you can scan the QR code on a website to perform a remote login.U
""")
                .padding()
                .lineLimit(3)
            Button(action: {
                appState.screenState = .scanning
                appState.isSpecialScreenState.toggle()
            }) {
                HStack(alignment: .center) {
                    Image(systemName: "qrcode.viewfinder")
                        .font(.largeTitle)
                        .foregroundColor(.white)
                    Text("Scan Login Code")
                    Spacer()
                    Image(systemName: "chevron.right")
                }
                .padding()
            }
        }
        .foregroundColor(.white)
        .background(Color.accentColor)
        .cornerRadius(20)
        .padding()
    }
    
    var settingsButton: some View {
        
        NavigationLink(destination: SettingsView()) {
            // "person.crop.circle"
            Image(systemName: "slider.horizontal.3")
                .imageScale(.large)
                .padding()
        }

    }
    
    var visitWebButton: some View {
        Button(action: {
            if let url = URL(string: "https://acme.spilikin.dev/") {
                UIApplication.shared.open(url)
            }
        }) {
            HStack(alignment: .center) {
                Image(systemName: "safari")
                    .imageScale(.large)
                    .foregroundColor(.accentColor)
                Text("Open website")

            }

        }
    }
}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
    }
}
