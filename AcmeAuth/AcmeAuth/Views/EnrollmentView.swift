// AcmeAuth/EnrollView.swift
// 


import SwiftUI
import Combine

struct EnrollmentView: View {
    let enrollmentManager = EnrollmentManager()
    @EnvironmentObject var appState: AppState
    @State private var showingErrorAlert = false
    @State private var errorMessage = ""
    @State var cancellable: AnyCancellable? = nil
    @State var useSmartcard = false
    @State var can = "123456"
    @State var pin = ""
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        VStack(alignment: .leading) {
            Spacer().frame(width: 1, height: 60)
            TextField("Account", text: $appState.settings.acct)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .font(.title)
                .padding()
            
            Toggle(isOn: $useSmartcard) {
                Text("Enroll using smartcard")
            }.padding()
            
            if (useSmartcard) {
                VStack (alignment: .leading) {
                    Text("CAN")
                    TextField("", text: $can)                .textFieldStyle(RoundedBorderTextFieldStyle())
                        .keyboardType(.numberPad)
                    Text("PIN")
                    SecureField("", text: $pin)                .textFieldStyle(RoundedBorderTextFieldStyle())
                        //.keyboardType(.numberPad)

                }
                .font(.title)
                .padding()
            }
            
            enrollButton
            
            Spacer()
        }
        .alert(isPresented: $showingErrorAlert) {
            errorAlert
        }
        .navigationBarTitle(Text("Enrollment"))
    }
    
    var enrollButton: some View {
        Button(action: {
            cancellable =  enrollmentManager.enroll(acct: appState.settings.acct)
                .receive(on: DispatchQueue.main)
                .sink(receiveCompletion: { completion in
                    switch completion {
                    case .finished:
                        break
                    case .failure(let error):
                        errorMessage = "Enrollment failed with error: \(error.localizedDescription)"
                        showingErrorAlert = true
                    }
                }, receiveValue: { str in
                    appState.settings.isEnrolled = true
                    appState.debugLog = ""
                    presentationMode.wrappedValue.dismiss()
                })

        }) {
            HStack(alignment: .center) {
                Image(systemName: "lock.shield.fill")
                    .font(.largeTitle)
                Text("Enroll")
                Spacer()
            }
            .foregroundColor(.white)
            .padding()
            
        }
        .background(Color.accentColor)
        .cornerRadius(15)
        .padding()
    }
    
    var errorAlert: Alert {
        Alert(
            title: Text("Error"),
            message: Text(errorMessage),
            dismissButton: .default(Text("Continue")) {
                showingErrorAlert = false
            })

    }

}

