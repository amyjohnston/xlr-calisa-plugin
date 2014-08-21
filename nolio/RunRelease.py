import sys, string, time
import com.xhaus.jyson.JysonCodec as json

RELEASE_CREATED_STATUS = 200

if nolioServer is None:
    print "No server provided."
    sys.exit(1)

nolioUrl = nolioServer['url']

credentials = CredentialsFallback(nolioServer, username, password).getCredentials()


content = """
{"releaseId":"%s","asynch":"%s","timeout":"%s"}
""" % (releaseId, str(asynch).lower(), str(timeout))

print "Sending content %s" % content

nolioAPIUrl = nolioUrl + '/datamanagement/a/api/run-release'

nolioResponse = XLRequest(nolioAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

if nolioResponse.status == RELEASE_CREATED_STATUS:
    data = json.loads(nolioResponse.read())
    releaseId = data.get('id')
    releaseDescrition = data.get('description')
    releaseResult = data.get('result')
    if releaseResult == False:
        print "Failed to run release in Nolio at %s." % nolioUrl
        nolioResponse.errorDump()
        sys.exit(1)
    print "Starting %s in Nolio at %s." % (releaseId, nolioUrl)
else:
    print "Failed to start release in Nolio at %s." % nolioUrl
    nolioResponse.errorDump()
    sys.exit(1)
