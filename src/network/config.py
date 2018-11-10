# Copyright 2009-2017 SAP SE or an SAP affiliate company.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# flake8: noqa

"""Contains the paths and attributes necessary for the integration tests."""
E2E_CONFIG = {
    'test-network': {
        'docker': {
            'compose_file_no_tls': 'test/fixtures/docker-compose-1peer-notls.yaml',
            'compose_file_tls': 'test/fixtures/docker-compose-2orgs-4peers-tls.yaml',
            'compose_file_tls_cli': 'test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml',
            'compose_file_trustas_minimal': 'test/fixtures/dc-trustas-minimal.yaml'
        },
        'channel-artifacts': {
            'channel_id': 'businesschannel',
            'channel.tx': 'test/fixtures/e2e_cli/channel-artifacts/channel.tx',
            'config_yaml': 'test/fixtures/e2e_cli/',
            'channel_profile': 'SingleOrgChannel'
        },
        'orderer': {
            'grpc_endpoint': 'localhost:7050',
            'server_hostname': 'orderer.example.com',
            'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/ordererOrganizations/'
                           'example.com/tlsca/tlsca.example.com-cert.pem',
            'mspid': 'OrdererMSP',
            'users': {
                'Admin': {
                    'cert': 'Admin@example.com-cert.pem',
                    'private_key': 'aca9d29a0056b2baab8692ed75e2487a38c84e6db86e651ec27cb7f97a8fdd9e_sk'}
            }
        },
        'org1.example.com': {
            'mspid': 'Org1MSP',
            'users': {
                'Admin': {
                    'cert': 'Admin@org1.example.com-cert.pem',
                    'private_key': '864f60da9c0aafa778658030a69ab4a844e305768cb65b77db05aedb8cbcc16d_sk'
                },
                'User1': {
                    'cert': 'User1@org1.example.com-cert.pem',
                    'private_key': 'a025dafac4b23f65d4529a3a37609edb3b99d90b0ceb250e4a65aeebe81aa84f_sk'
                }
            },
            'peers': {
                'as000': {
                    'grpc_request_endpoint': 'localhost:7051',
                    'grpc_event_endpoint': 'localhost:7053',
                    'server_hostname': 'as000.org1.example.com',
                    'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/peerOrganizations/'
                                   'org1.example.com/peers/as000.org1.example.com/msp/tlscacerts/'
                                   'tlsca.org1.example.com-cert.pem'
                }
            }
        }
        #,
        # 'org2.example.com': {
        #     'mspid': 'Org2MSP',
        #     'users': {
        #         'Admin': {
        #             'cert': 'Admin@org2.example.com-cert.pem',
        #             'private_key': 'a23db9fe4fdfc7d8f87a42919597b44e52b429fb09634b523b366146b9bf1e3b_sk'
        #         },
        #         'User1': {
        #             'cert': 'User1@org2.example.com-cert.pem',
        #             'private_key': '90da90b106c077543acc5b5f414ee857a3d5b1096d7be11f6f2ec25787e5110b_sk'
        #         }
        #     },
        #     'peers': {
        #         'peer0': {
        #             'grpc_request_endpoint': 'localhost:9051',
        #             'grpc_event_endpoint': 'localhost:9053',
        #             'server_hostname': 'peer0.org2.example.com',
        #             'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/peerOrganizations/'
        #                            'org2.example.com/peers/peer0.org2.example.com/msp/tlscacerts/'
        #                            'tlsca.org2.example.com-cert.pem'
        #         }
        #     }
        # }
    }
}
