""" Tests for main.py """

import pytest
from asyncio import IncompleteReadError
from unittest.mock import AsyncMock, Mock
import os
from hl7_listener import main
import importlib
from nats.aio.client import Client as NATS_Client
from nats.aio.errors import ErrNoServers

package_directory = os.path.dirname(os.path.abspath(__file__))
print(package_directory)
root_path = "/../resources"
config_file = os.path.join(package_directory + root_path, "config.ini")
_hl7_messages_relative_dir = os.path.join(package_directory + root_path, "hl7_messages")


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    os.environ["HL7_MLLP_HOST"] = "hl7-mllp-host"
    os.environ["HL7_MLLP_PORT"] = "4444"
    os.environ["NATS_SERVER_URL"] = "nats-server"

    importlib.reload(main)


@pytest.mark.asyncio
async def test_nc_connect(mocker):
    mocker.patch.object(NATS_Client, "connect")
    result = await main.nc_connect()
    assert result is True

    NATS_Client.connect.side_effect = ErrNoServers()
    with pytest.raises(ErrNoServers):
        await main.nc_connect()


@pytest.mark.asyncio
async def test_send_msg_to_nats(mocker):
    mocker.patch.object(main, "_js")
    my_asyncmock = AsyncMock()
    mocker.patch.object(main._js, "publish", new=my_asyncmock)
    await main.send_msg_to_nats("test message")
    my_asyncmock.assert_awaited()


@pytest.mark.asyncio
async def test_processed_received_hl7_messages(mocker):
    with open(_hl7_messages_relative_dir + "/adt-a01-sample01.hl7", "r") as file:
        hl7_text = str(file.read())

    # Mock reader input parameter.
    asyncmock_reader = AsyncMock()
    asyncmock_reader.at_eof = Mock()
    asyncmock_reader.at_eof.side_effect = [False, True]
    mock_hl7_message = Mock()
    mocker.patch.object(mock_hl7_message, "__str__", return_value=hl7_text)
    mocker.patch.object(mock_hl7_message, "create_ack", return_value="ack")
    mocker.patch.object(asyncmock_reader, "readmessage", return_value=mock_hl7_message)

    # Mock writer input parameter.
    asyncmock_writer = AsyncMock()
    mocker.patch.object(
        asyncmock_writer, "get_extra_info", return_value="test_hl7_peername"
    )
    mocker.patch.object(asyncmock_writer, "writemessage")
    mocker.patch.object(asyncmock_writer, "drain")

    mocker.patch.object(main, "send_msg_to_nats", new=AsyncMock())

    # Above mocks setup to test the "happy" path.
    #
    await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)
    # Expect default "Application Accept" (AA) ack_code.
    mock_hl7_message.create_ack.assert_called_once_with()
    asyncmock_writer.writemessage.assert_called_once_with("ack")
    asyncmock_writer.drain.assert_called_once()

    # Test force hl7 parse exception.
    # The exception should be handled and an Application Reject (AR) ack_code returned.
    #
    asyncmock_reader.reset_mock()
    asyncmock_reader.at_eof.side_effect = [False, True]
    asyncmock_writer.reset_mock()
    mock_hl7_message.reset_mock()
    # Last param needed to save mock calls.
    mocker.patch.object(mock_hl7_message, "create_ack", mock_hl7_message)
    mocker.patch.object(mock_hl7_message, "__str__", return_value="not an hl7 message")
    await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)
    assert "ack_code='AR'" in str(mock_hl7_message.mock_calls[0])

    # Test asyncio.IncompleteReadError.
    # The exception is raised with this scenario.
    #
    asyncmock_reader.reset_mock()
    asyncmock_reader.at_eof.side_effect = [False, False]
    asyncmock_reader.readmessage.side_effect = IncompleteReadError(
        "some bytes".encode(), 22
    )
    with pytest.raises(IncompleteReadError):
        await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)

    # Test general Exception after hl7_message is defined. This should result in
    # an Application Error (AE) ack_code and no raised exception.
    #
    asyncmock_reader.reset_mock()
    asyncmock_reader.at_eof.side_effect = [False, True]
    asyncmock_reader.readmessage.side_effect = None
    asyncmock_writer.reset_mock()
    mock_hl7_message.reset_mock()
    # Last param needed to save mock calls.
    mocker.patch.object(mock_hl7_message, "create_ack", mock_hl7_message)
    mocker.patch.object(mock_hl7_message, "__str__", return_value=hl7_text)
    main.send_msg_to_nats.side_effect = Exception("force exception from mock")
    await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)
    assert "ack_code='AE'" in str(mock_hl7_message.mock_calls[0])


@pytest.mark.asyncio
async def test_hl7_receiver_exception(mocker):
    # Session config parameters should result in a connection error that raises an Exception.
    with pytest.raises(Exception):
        await main.hl7_receiver()
