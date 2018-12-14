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
    'trustas-network': {
        'docker': {
            'compose_file_no_tls': 'test/fixtures/docker-compose-1peer-notls.yaml',
            'compose_file_tls': 'test/fixtures/docker-compose-2orgs-4peers-tls.yaml',
            'compose_file_tls_cli': 'test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml',
            'compose_file_trustas_gcp': 'test/fixtures/dc-trustas-gcp.yaml',
            'compose_file_trustas_localhost': 'test/fixtures/dc-trustas-localhost.yaml'
            # 'compose_file_trustas_localhost': 'test/fixtures/dc-local-10peers.yaml'
            # 'compose_file_trustas_localhost': 'test/fixtures/dc-local-2orgs-4peers.yaml'
        },
        'channel-artifacts': {
            'channel_id': 'businesschannel',
            'channel.tx': 'test/fixtures/e2e_cli/channel-artifacts/channel.tx',
            'config_yaml': 'test/fixtures/e2e_cli/',
            'channel_profile': 'SingleOrgChannel'
        },
        'orderer': {
            'gcp_grpc_endpoint': 'orderer.us-east1-b.c.trust-as.internal:7050',
            'local_grpc_endpoint': 'localhost:7050',
            'server_hostname': 'orderer.example.com',
            'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/ordererOrganizations/'
                           'example.com/tlsca/tlsca.example.com-cert.pem',
            'mspid': 'OrdererMSP',
            'users': {
                'Admin': {
                    'cert': 'Admin@example.com-cert.pem',
                    'private_key': 'b92d5923828aa15d965e438de5a7edb92ec128889c2fe8026ee7b95490270048_sk'}
            }
        },
        'org1.example.com': {
            'mspid': 'Org1MSP',
            'users': {
                'Admin': {
                    'cert': 'Admin@org1.example.com-cert.pem',
                    'private_key': '570182787133a5137f0982ba0e018462d3ed20491402585741bb516922fc9416_sk'
                },
                'User1': {
                    'cert': 'User1@org1.example.com-cert.pem',
                    'private_key': '613ca29ff265101aaebd9b79aff9924d5cd7baa9077141d24cf7c8fed4425bd4_sk'
                }
            },
            'peers': {
                'peer0': {
                    'gcp_grpc_request_endpoint': 'peer0.us-east1-b.c.trust-as.internal:7051',
                    'gcp_grpc_event_endpoint': 'peer0.us-east1-b.c.trust-as.internal:7053',
                    'local_grpc_request_endpoint': 'localhost:7051',
                    'local_grpc_event_endpoint': 'localhost:7053',
                    'server_hostname': 'peer0.org1.example.com',
                    'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/peerOrganizations/'
                                   'org1.example.com/peers/peer0.org1.example.com/msp/tlscacerts/'
                                   'tlsca.org1.example.com-cert.pem'
                },
                # 'peer1': {
                #     'gcp_grpc_request_endpoint': 'peer1.us-east1-b.c.trust-as.internal:7051',
                #     'gcp_grpc_event_endpoint': 'peer1.us-east1-b.c.trust-as.internal:7053',
                #     'local_grpc_request_endpoint': 'localhost:8051',
                #     'local_grpc_event_endpoint': 'localhost:8053',
                #     'server_hostname': 'peer1.org1.example.com',
                #     'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/peerOrganizations/'
                #                    'org1.example.com/peers/peer1.org1.example.com/msp/tlscacerts/'
                #                    'tlsca.org1.example.com-cert.pem'
                # },
                # 'peer2': {
                #     'gcp_grpc_request_endpoint': 'peer2.us-east1-b.c.trust-as.internal:7051',
                #     'gcp_grpc_event_endpoint': 'peer2.us-east1-b.c.trust-as.internal:7053',
                #     'local_grpc_request_endpoint': 'localhost:9051',
                #     'local_grpc_event_endpoint': 'localhost:9053',
                #     'server_hostname': 'peer2.org1.example.com',
                #     'tls_cacerts': 'test/fixtures/e2e_cli/crypto-config/peerOrganizations/'
                #                    'org1.example.com/peers/peer2.org1.example.com/msp/tlscacerts/'
                #                    'tlsca.org1.example.com-cert.pem'
                # }
            }
        }
    }
}
