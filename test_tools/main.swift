//
//  main.swift
//  F1Receiver
//
//  Created by Ryan Quinlan on 2/22/20.
//  Copyright © 2020 Ryan Quinlan. All rights reserved.
//

import Foundation
import SwiftSocket

print("Hello Wookie!")

//func echoService(client: TCPClient) {
//    print("Newclient from:\(client.address)[\(client.port)]")
//    let d = client.read(1024*10)
//    client.send(data: d!)
//    client.close()
//}
//
//func testServer() {
//    let server = TCPServer(address: "0.0.0.0", port: 8080)
//    switch server.listen() {
//      case .success:
//        while true {
//            if var client = server.accept() {
//                echoService(client: client)
//            } else {
//                print("accept error")
//            }
//        }
//      case .failure(let error):
//        print(error)
//    }
//}

func testServer() {
    let server = UDPServer(address: "0.0.0.0", port: 8080)
    while true {
        let(b, ip, port) = server.recv(1024)
        print("packet!")
        print(b)
    }

}

testServer()
