import SwiftUI
import Combine

struct HomeView: View {
    @EnvironmentObject var appState: AppState
    @State var showingScanner = false
    @State var showingLogin = false
    
    func debug(_ text: String) {
        self.appState.debugLog = text + "\n" + self.appState.debugLog
    }
    
    var body: some View {
        NavigationView {
            VStack(alignment: .center) {
                scannerButton
                readCardButton
                visitWebButton
                debugView
                Spacer()
            }
            .navigationBarTitle(Text("Acme Companion"))
            .navigationBarItems(trailing: settingsButton)
            .sheet(isPresented: $showingScanner) {
                ScannerView(showSheetView: self.$showingScanner)
            }
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

            }.padding()
                .foregroundColor(.white)
                .background(Color.accentColor)
                .cornerRadius(40)
        }

    }
    
    var header: some View {
        HStack(alignment: .center) {
            Spacer().frame(width: 50)
            Text("Acme Authenticator")
                .font(.title)
                .frame(maxWidth: .infinity)
            settingsButton
        }
    }
    
    var debugView: some View {
        Text(self.appState.debugLog)
            .font(Font.system(.footnote, design: .monospaced))
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
    }
    
    var scannerButton: some View {
        
        Button(action: {
            self.showingScanner.toggle()
        }) {
            HStack(alignment: .center) {
                Image(systemName: "qrcode.viewfinder")
                    .font(.largeTitle)
                    .foregroundColor(.white)
                Text("Scan Login Code")

            }.padding()
                .foregroundColor(.white)
                .background(Color.accentColor)
                .cornerRadius(40)
        }.sheet(isPresented: $showingScanner) {
            ScannerView(showSheetView: self.$showingScanner)
        }
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
