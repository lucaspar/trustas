E2E_CONFIG = {

    'trustas-net': {
        'docker': {
            'compose_file_tls': 'test/fixtures/dc-trustas.yaml'
        },
        'channel-artifacts': {
            'channel_id': 'businesschannel',
            'channel.tx': 'test/fixtures/trustas/channel-artifacts/channel.tx',
            'config_yaml': 'test/fixtures/trustas/',
            'channel_profile': 'TrustASChannel'
        },
        'orderer': {
            'grpc_endpoint': 'localhost:7050',
            'server_hostname': 'orderer.example.com',
            'tls_cacerts': 'test/fixtures/trustas/crypto-config/ordererOrganizations/'
                           'example.com/tlsca/tlsca.example.com-cert.pem',
            'mspid': 'OrdererMSP',
            'users': {
                'Admin': {
                    'cert': 'Admin@example.com-cert.pem',
                    # crypto-config/ordererOrganizations/example.com/users/Admin@example.com/msp/keystore
                    'private_key': '630e3767a6e1d3c8e646460123d397455103a900efb4d6fb679a9d9c481841fc_sk'}
            }
        },
        'org1.example.com': {
            'mspid': 'Org1MSP',
            'users': {
                'Admin': {
                    'cert': 'Admin@org1.example.com-cert.pem',
                    # crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore
                    'private_key': '39f2beaa658649a1b647ab1d9e5d09d8b500a7a3b72ee0e3e606f9ed07db98c9_sk'
                },
                'User1': {
                    'cert': 'User1@org1.example.com-cert.pem',
                    # crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore
                    'private_key': 'e03767a909cd9361b004fb27213fc2fba57519d436c46dd8665595825929e982_sk'
                }
            },
            'peers': {
                'peer0': {
                    'grpc_request_endpoint': 'localhost:7051',
                    'grpc_event_endpoint': 'localhost:7053',
                    'server_hostname': 'peer0.org1.example.com',
                    'tls_cacerts': 'test/fixtures/trustas/crypto-config/peerOrganizations/'
                                   'org1.example.com/peers/peer0.org1.example.com/msp/tlscacerts/'
                                   'tlsca.org1.example.com-cert.pem'
                }
            }
        },
        'org2.example.com': {
            'mspid': 'Org2MSP',
            'users': {
                'Admin': {
                    'cert': 'Admin@org2.example.com-cert.pem',
                    'private_key': '51cb59780ee7426a3802ded2bf6af75d82c181cbd5794cf405777c833b571098_sk'
                },
                'User1': {
                    'cert': 'User1@org2.example.com-cert.pem',
                    'private_key': '3790419c14d683ce661d02fa039c338e608809d5507770b22ac1764c6350b61d_sk'
                }
            },
            'peers': {
                'peer0': {
                    'grpc_request_endpoint': 'localhost:7151',
                    'grpc_event_endpoint': 'localhost:7153',
                    'server_hostname': 'peer0.org2.example.com',
                    'tls_cacerts': 'test/fixtures/trustas/crypto-config/peerOrganizations/'
                                   'org2.example.com/peers/peer0.org2.example.com/msp/tlscacerts/'
                                   'tlsca.org2.example.com-cert.pem'
                }
            }
        },
        'org3.example.com': {
            'mspid': 'Org3MSP',
            'users': {
                'Admin': {
                    'cert': 'Admin@org3.example.com-cert.pem',
                    'private_key': '5dd9e62560c5f6985bbbaf86cf2cf664a39ee9414e4659916e1216f55221c920_sk'
                },
                'User1': {
                    'cert': 'User1@org3.example.com-cert.pem',
                    'private_key': '64aadada0d4c907b41a428a90be3a08c7ff363c8a9489bf34c2b1f62eb3aa425_sk'
                }
            },
            'peers': {
                'peer0': {
                    'grpc_request_endpoint': 'localhost:7251',
                    'grpc_event_endpoint': 'localhost:7253',
                    'server_hostname': 'peer0.org3.example.com',
                    'tls_cacerts': 'test/fixtures/trustas/crypto-config/peerOrganizations/'
                                   'org3.example.com/peers/peer0.org3.example.com/msp/tlscacerts/'
                                   'tlsca.org3.example.com-cert.pem'
                }
            }
        },
    },

    ##################
    ##################

    # '3org-net': {
    #     'docker': {
    #         # 'compose_file_no_tls': 'test/fixtures/docker-compose-1peer-notls.yaml',
    #         # 'compose_file_tls_cli': 'test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml',
    #         'compose_file_tls': 'test/fixtures/dc-trustas.yaml'
    #     },
    #     'channel-artifacts': {
    #         'channel_id': 'businesschannel',
    #         'channel.tx': 'test/fixtures/trustas/channel-artifacts/channel.tx',
    #         'config_yaml': 'test/fixtures/trustas/',
    #         'channel_profile': 'TrustASChannel'
    #     },
    #     'orderer': {
    #         'grpc_endpoint': 'localhost:7050',
    #         'server_hostname': 'orderer.example.com',
    #         'tls_cacerts': 'test/fixtures/trustas/crypto-config/ordererOrganizations/'
    #                        'example.com/tlsca/tlsca.example.com-cert.pem',
    #         'mspid': 'OrdererMSP',
    #         'users': {
    #             'Admin': {
    #                 'cert': 'Admin@example.com-cert.pem',
    #                 # crypto-config/ordererOrganizations/example.com/users/Admin@example.com/msp/keystore
    #                 'private_key': '630e3767a6e1d3c8e646460123d397455103a900efb4d6fb679a9d9c481841fc_sk'}
    #         }
    #     },
    #     'org1.example.com': {
    #         'mspid': 'Org1MSP',
    #         'users': {
    #             'Admin': {
    #                 'cert': 'Admin@org1.example.com-cert.pem',
    #                 # crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore
    #                 'private_key': '39f2beaa658649a1b647ab1d9e5d09d8b500a7a3b72ee0e3e606f9ed07db98c9_sk'
    #             },
    #             'User1': {
    #                 'cert': 'User1@org1.example.com-cert.pem',
    #                 # crypto-config/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore
    #                 'private_key': 'e03767a909cd9361b004fb27213fc2fba57519d436c46dd8665595825929e982_sk'
    #             }
    #         },
    #         'peers': {
    #             'peer0': {
    #                 'grpc_request_endpoint': 'localhost:7051',
    #                 'grpc_event_endpoint': 'localhost:7053',
    #                 'server_hostname': 'peer0.org1.example.com',
    #                 'tls_cacerts': 'test/fixtures/trustas/crypto-config/peerOrganizations/'
    #                                'org1.example.com/peers/peer0.org1.example.com/msp/tlscacerts/'
    #                                'tlsca.org1.example.com-cert.pem'
    #             }
    #         }
    #     },
    #     'org2.example.com': {
    #         'mspid': 'Org2MSP',
    #         'users': {
    #             'Admin': {
    #                 'cert': 'Admin@org2.example.com-cert.pem',
    #                 'private_key': '51cb59780ee7426a3802ded2bf6af75d82c181cbd5794cf405777c833b571098_sk'
    #             },
    #             'User1': {
    #                 'cert': 'User1@org2.example.com-cert.pem',
    #                 'private_key': '3790419c14d683ce661d02fa039c338e608809d5507770b22ac1764c6350b61d_sk'
    #             }
    #         },
    #         'peers': {
    #             'peer0': {
    #                 'grpc_request_endpoint': 'localhost:8051',
    #                 'grpc_event_endpoint': 'localhost:8053',
    #                 'server_hostname': 'peer0.org2.example.com',
    #                 'tls_cacerts': 'test/fixtures/trustas/crypto-config/peerOrganizations/'
    #                                'org2.example.com/peers/peer0.org2.example.com/msp/tlscacerts/'
    #                                'tlsca.org2.example.com-cert.pem'
    #             }
    #         }
    #     },
    #     'org3.example.com': {
    #         'mspid': 'Org3MSP',
    #         'users': {
    #             'Admin': {
    #                 'cert': 'Admin@org3.example.com-cert.pem',
    #                 'private_key': '5dd9e62560c5f6985bbbaf86cf2cf664a39ee9414e4659916e1216f55221c920_sk'
    #             },
    #             'User1': {
    #                 'cert': 'User1@org3.example.com-cert.pem',
    #                 'private_key': '64aadada0d4c907b41a428a90be3a08c7ff363c8a9489bf34c2b1f62eb3aa425_sk'
    #             }
    #         },
    #         'peers': {
    #             'peer0': {
    #                 'grpc_request_endpoint': 'localhost:9051',
    #                 'grpc_event_endpoint': 'localhost:9053',
    #                 'server_hostname': 'peer0.org3.example.com',
    #                 'tls_cacerts': 'test/fixtures/trustas/crypto-config/peerOrganizations/'
    #                                'org3.example.com/peers/peer0.org3.example.com/msp/tlscacerts/'
    #                                'tlsca.org3.example.com-cert.pem'
    #             }
    #         }
    #     },
    # },


    # ########################
    # ########################


    # 'test-network': {
    #     'docker': {
    #         'compose_file_no_tls': 'test/fixtures/docker-compose-1peer-notls.yaml',
    #         'compose_file_tls': 'test/fixtures/docker-compose-2orgs-4peers-tls.yaml',
    #         'compose_file_tls_cli': 'test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml'
    #     },
    #     'channel-artifacts': {
    #         'channel_id': 'businesschannel',
    #         'channel.tx': 'test/fixtures/e2e_cli/channel-artifacts/channel.tx',
    #         'config_yaml': 'test/fixtures/e2e_cli/',
    #         'channel_profile': 'TwoOrgsChannel'
    #     },
    #     'orderer': {
    #         'grpc_endpoint': 'localhost:7050',
    #         'server_hostname': 'orderer.example.com',
    #         'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/ordererOrganizations/'
    #                        'example.com/tlsca/tlsca.example.com-cert.pem',
    #         'mspid': 'OrdererMSP',
    #         'users': {
    #             'Admin': {
    #                 'cert': 'Admin@example.com-cert.pem',
    #                 'private_key': '630e3767a6e1d3c8e646460123d397455103a900efb4d6fb679a9d9c481841fc_sk'}
    #         }
    #     },
    #     'org1.example.com': {
    #         'mspid': 'Org1MSP',
    #         'users': {
    #             'Admin': {
    #                 'cert': 'Admin@org1.example.com-cert.pem',
    #                 'private_key': 'c76527489d5820bd04da80a84c07033ca574413f80614091e04f05c276fb6896_sk'
    #             },
    #             'User1': {
    #                 'cert': 'User1@org1.example.com-cert.pem',
    #                 'private_key': 'da72fd6c0f4595d33eb9ae6f6d06cd171ebc3882fc856960c244b9b5c2b35a90_sk'
    #             }
    #         },
    #         'peers': {
    #             'peer0': {
    #                 'grpc_request_endpoint': 'localhost:7051',
    #                 'grpc_event_endpoint': 'localhost:7053',
    #                 'server_hostname': 'peer0.org1.example.com',
    #                 'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/peerOrganizations/'
    #                                'org1.example.com/peers/peer0.org1.example.com/msp/tlscacerts/'
    #                                'tlsca.org1.example.com-cert.pem'
    #             }
    #         }
    #     },
    #     'org2.example.com': {
    #         'mspid': 'Org2MSP',
    #         'users': {
    #             'Admin': {
    #                 'cert': 'Admin@org2.example.com-cert.pem',
    #                 'private_key': '7e0b1c172161fe0f33603106935d2584918e12af955108e429dd63d4c043067a_sk'
    #             },
    #             'User1': {
    #                 'cert': 'User1@org2.example.com-cert.pem',
    #                 'private_key': '73beefad9003c589064deb2128c4f0831ba8003f1233102cc52a188afd05fe61_sk'
    #             }
    #         },
    #         'peers': {
    #             'peer0': {
    #                 'grpc_request_endpoint': 'localhost:9051',
    #                 'grpc_event_endpoint': 'localhost:9053',
    #                 'server_hostname': 'peer0.org2.example.com',
    #                 'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/peerOrganizations/'
    #                                'org2.example.com/peers/peer0.org2.example.com/msp/tlscacerts/'
    #                                'tlsca.org2.example.com-cert.pem'
    #             }
    #         }
    #     }
    # }
}
