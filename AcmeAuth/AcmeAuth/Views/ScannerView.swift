// AcmeAuth/ScannerView.swift
// 


import SwiftUI
import CodeScanner

struct ScannerView: View {
    @Binding var showSheetView: Bool

    var body: some View {
        NavigationView {
            CodeScannerView(codeTypes: [.qr], simulatedData: "https://appauth.acme.spilikin.dev/challenge?nonce=ABCDEFG", completion: self.handleScan)
            .navigationBarTitle(Text("Scan Login Code"), displayMode: .inline)
            .navigationBarItems(trailing: Button(action: {
                self.showSheetView = false
            }) {
                Image(systemName: "multiply.circle.fill")
                    .imageScale(.large)
                    .padding()
            })
        }
    }

    func handleScan(result: Result<String, CodeScannerView.ScanError>) {
        print (result)
        //self.showSheetView = false
    }
    

}
