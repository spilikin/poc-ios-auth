// AcmeAuth/NFCUtility.swift
// 


import CoreNFC
import Combine

typealias CardInfoCompletition = (Result<String, Error>) -> Void

enum NFCError: LocalizedError {
    case unavailable
    case timeout
    case cardNotFound

    
    var errorDescription: String? {
        switch self {
        case .unavailable:
            return "NFC Reader Not Available"
        case .timeout:
            return "Timeout occured"
        case .cardNotFound:
            return "Card not found"
        }
    }

}


class NFCUtility: NSObject {
    private var session: NFCTagReaderSession?
    private var completition: CardInfoCompletition?
    
    public func pollCardInfo(_ completition: @escaping CardInfoCompletition) {
        self.completition = completition
        startCardPolling()
    }
    
    public func startCardPolling() {

        guard NFCTagReaderSession.readingAvailable else {
            print("NFC is not available on this device")
            completition?(.failure(NFCError.unavailable))
            return
        }
        
        session = NFCTagReaderSession(pollingOption: .iso14443, delegate: self)
        session?.alertMessage = "Hold a smartcard next to your device"
        session?.begin()

    }
    
    func invalidateSession() {
        session?.invalidate()
        session = nil
    }
}



extension NFCUtility: NFCTagReaderSessionDelegate {
    public func tagReaderSessionDidBecomeActive(_ session: NFCTagReaderSession) {
     }

     public func tagReaderSession(_ session: NFCTagReaderSession, didInvalidateWithError error: Swift.Error) {
        print("tagReaderSession:didInvalidateWithError: \(error)")
        if let nfcerror = error as? NFCReaderError {
            print (nfcerror.errorCode)
        }
        invalidateSession()
     }

     public func tagReaderSession(_ session: NFCTagReaderSession, didDetect tags: [NFCTag]) {
        

        guard let tag = tags.first else {
            session.alertMessage = "Card not found"
            return
        }

        guard case .iso7816(let smartcard) = tag else {
            session.alertMessage = "Invalid card"
            return
        }

        
        session.alertMessage = "Connecting"

        // Connect to tag
        session.connect(to: tag) { [unowned self] (error: Swift.Error?) in
            if error != nil {
                self.invalidateSession()
                return
            }
            
            // Smartcard Karate would start here here
            // since it's only a PoC we just put delay here
            let apdu = NFCISO7816APDU(instructionClass: 0, instructionCode: 0, p1Parameter: 0, p2Parameter: 0, data: Data(), expectedResponseLength: 256)
            for num in 1...500 {
                smartcard.sendCommand(apdu: apdu, completionHandler: { lData, lSw1, lSw2, err in
                    if let _ = err {
                        smartcard.session?.invalidate(errorMessage: "Error during smartcard Karate")
                    } else {
                        session.alertMessage = "\(num)/500"
                    }
                    if (num == 500) {
                        session.alertMessage = "Done"
                        smartcard.session?.invalidate()
                    }
                })
            }
            
            /*
            session.alertMessage = "Connected to smartcard"
            DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                session.alertMessage = "Doing smartcard Karate"
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                session.alertMessage = "Even more smartcard Karate"
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 4) {
                session.alertMessage = "Almost there"
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 5) {
                session.alertMessage = "Done"
                smartcard.session?.invalidate()
            }
            */
         }
     }
}
