import ssl
import sys
import sslpsk
from sslpsk.sslpsk import _ssl_set_psk_server_callback, _ssl_set_psk_client_callback

# Monkey patch for SSLPSK
def _sslobj(sock):
    if (3, 5) <= sys.version_info <= (3, 7):
        return sock._sslobj._sslobj
    else:
        return sock._sslobj

sslpsk.sslpsk._sslobj = _sslobj

def on_connect(client, user_data, flags, rc):
    print("result code : ${}".format(str(rc)))
    client.subscribe("sci-topic")    


def on_message(client, user_data, msg):
    print(msg.topic + "")



def _ssl_setup_psk_callbacks(sslobj):
    psk = sslobj.context.psk
    hint = sslobj.context.hint
    if psk:
        if sslobj.server_side:
            cb = psk if callable(psk) else lambda _identity: psk
            _ssl_set_psk_server_callback(sslobj, cb, hint)
        else:
            cb = psk if callable(psk) else lambda _hint: psk if isinstance(psk, tuple) else (psk, b"")
            _ssl_set_psk_client_callback(sslobj, cb)


class SSLPSKContext(ssl.SSLContext):
    @property
    def psk(self):
        return getattr(self, "_psk", None)

    @psk.setter
    def psk(self, psk):
        self._psk = psk

    @property
    def hint(self):
        return getattr(self, "_hint", None)

    @hint.setter
    def hint(self, hint):
        self._hint = hint


class SSLPSKObject(ssl.SSLObject):
    def do_handshake(self, *args, **kwargs):
        _ssl_setup_psk_callbacks(self)
        super().do_handshake(*args, **kwargs)


class SSLPSKSocket(ssl.SSLSocket):
    def do_handshake(self, *args, **kwargs):
        _ssl_setup_psk_callbacks(self)
        super().do_handshake(*args, **kwargs)


SSLPSKContext.sslobject_class = SSLPSKObject
SSLPSKContext.sslsocket_class = SSLPSKSocket
