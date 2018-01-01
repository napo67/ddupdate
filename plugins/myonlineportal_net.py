'''
ddupdate plugin updating data on myonlineportal.net

See: ddupdate(8)
See: http://myonlineportal.net/ddns_api
'''

from ddupdate.plugins_base import UpdatePlugin, UpdateError, \
    get_response, http_basic_auth_setup


class MyOnlinePortalPlugin(UpdatePlugin):
    '''
    Updates DNS data for host on myonlineportal.net  As usual, any host
    updated must first be defined in the web UI. Providing an ip address
    is optional but supported; the ip-disabled plugin can be used.

    netrc: Use a line like
        machine myonlineportal.net login <username> password <password>

    Options:
        None
    '''
    _name = 'myonlineportal.net'
    _oneliner = 'Updates on http://myonlineportal.net/'
    _url = 'https://myonlineportal.net/updateddns?hostname={0}'

    def run(self, config, log, ip=None):

        url = self._url.format(config.hostname)
        if ip:
            url += "&ip=" + ip.v4
        http_basic_auth_setup(url, 'myonlineportal.net')
        html = get_response(log, url)
        log.info("Server reply: " + html)
        key = html.split()[0]
        if key not in ['OK', 'nochg']:
            raise UpdateError("Bad server reply: " + html)
        log.info("server reply: " + html)
