import SwiftUI

import CoreNFC

struct SettingsView: View {

    var body: some View {
        ScrollView {
            VStack(alignment: .center) {
                Text("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc maximus quam quis euismod semper. Vivamus eleifend lacus vel est consectetur tristique. Proin eu dolor diam. Duis elementum accumsan fringilla. In metus diam, euismod facilisis nibh at, tristique rutrum est. Sed sit amet congue dui. Nulla tempus nisi at laoreet feugiat. Mauris sodales leo quis velit dignissim tincidunt. Quisque in leo ut felis sodales semper id non magna. Vestibulum et ornare nisi. Ut congue sagittis ipsum id imperdiet. Maecenas ac efficitur metus, sed mattis mi.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam molestie pulvinar sapien, vel gravida lorem. Suspendisse est massa, aliquet eu laoreet ac, malesuada vel magna. Pellentesque sed ornare nisl. Morbi at ullamcorper nisl. Phasellus viverra feugiat risus, a egestas elit viverra vitae. Curabitur scelerisque pretium eros, quis fringilla eros molestie eleifend. Phasellus placerat et mauris vestibulum commodo. Donec orci diam, fringilla eu arcu eu, hendrerit euismod purus. Donec a diam at ligula ornare cursus. Donec at vestibulum mauris, non commodo purus. Aenean auctor magna a justo consectetur fringilla.

Sed eu tellus ligula. In hac habitasse platea dictumst. Fusce pretium porttitor ornare. Nullam at consectetur ligula. Integer nec justo sapien. Duis sed est dolor. Phasellus dapibus tincidunt dui, ut accumsan orci consectetur vitae. Ut at nisi orci. Etiam libero sapien, luctus vitae felis a, maximus molestie lacus. Nunc nisi dolor, pharetra sit amet tortor sed, lobortis rhoncus arcu. Donec varius risus ac quam egestas, in maximus ligula mollis. Fusce lacinia, mauris ac convallis lobortis, turpis urna tempor turpis, vel ultricies magna neque in metus. Morbi nisl neque, rutrum vitae turpis in, commodo pretium neque. Integer elementum nunc lectus, id congue massa condimentum vestibulum. Suspendisse vulputate metus a tincidunt ultricies. Suspendisse eget hendrerit neque, non condimentum neque.
""")
                Spacer()
            }
            .navigationBarTitle(Text("Settings"))
        }
    }

}

