#!usr/bin/python
# -*- coding: utf-8 -*-

import hashlib, time, random, types, traceback, os, sys
import logging

class LogNI:

	def __init__( self ):
		
		self.__stderr	= 0
		self.__flush	= 1
		self.__maxLen	= 1000
		self.__strip	= 0
		self.__stackOffset=0
		self.__stackDepth= 1
		self.__timeFormat= '%Y/%m/%d %H:%M:%S'

		self.__fd	= None
		self.__charset	= 'utf8'

		self.__logEntries = 0


	def logentries( self, apiKey ):

		# logentries 
		try:
			from logentries import LogentriesHandler
		except Exception, emsg:
			self.ni( 'logentries import error="%s"', emsg, ERR=4 )
			return

		self.__loge = logging.getLogger('logentries')
		self.__loge.setLevel(logging.INFO)
		# Note if you have set up the logentries handler in Django, the following line is not necessary
		self.__loge.addHandler(LogentriesHandler( apiKey ))

		self.__logEntries = 1


	def file( self, logFile):

		try:
			self.__fd = open( logFile, 'ab' )
		except Exception, emsg:
			sys.stderr.write( 'logni: file="%s", open err="%s"', (logFile, emsg) )
			return 0

		return 1


	def mask( self, maskStr='' ):
		
		if maskStr == 'ALL':
			maskStr = 'I1E1F1W1D1'

		if len(maskStr) % 2 != 0:
			raise ValueError( 'logni: incorrect mask="%s"' % (maskStr,) )

		for no in range( 0, len(maskStr), 2):
			
			logType	 = maskStr[ no   ]
			logLevel = maskStr[ no+1 ]
		
			if not logLevel.isdigit():
				raise ValueError( 'logni: logLevel="%s" must be integer' % (logLevel,) )


	def stderr( self, stderr=0):
		self.__stderr = stderr

	def flush( self, flush=0):
		self.__flush = flush

	def strip( self, strip=0):
		self.__strip = strip

	def maxLen( self, maxLen=0):
		self.__maxLen = maxLen


	def __le( self, msg, mask ):
		# logentries
		if mask == 'INFO':
			self.__loge.info( msg )

		elif mask == 'WARN':
			self.__loge.warning( msg )

		elif mask == 'ERR':
			self.__loge.error( msg )

		elif mask == 'FATAL':
			self.__loge.critical( msg )

		elif mask == 'DEBUG':
			self.__loge.debug( msg )


	def ni( self, msg, params={}, offset=0, depth=0, color='', maxLen=0, **kw ):

		mask, level = kw.iteritems().next()
		logInfo = '%s%s' % (mask[0], level)

		try:
			msg = msg % params
		except Exception, emsg:
			logInfo	= '!!'
			color	= 'red'
			msg   	= '%s %s <%s>' % (msg, params, emsg)
		
		# unicode test
		if type( msg ) == types.UnicodeType:
			msg = msg.encode( self.__charset, 'ignore' )
		
		# strip text
		if self.__strip:
			msg = msg.replace( '\n', ' ' ).strip()

		# stack
        	stackList = []
        	offset = (offset or self.__stackOffset or 0) + 1
        	limit  = (depth or self.__stackDepth) + offset
        	for ( filename, line, func, text ) in traceback.extract_stack( limit=limit )[ : -offset ]:
                	filename = filename.split( '/' )[ -1 ]
                	lineInfo = "%s:%s():%s" % ( filename, func, line )
                	stackList.append( lineInfo )
        	stackInfo = ",".join(stackList)

		# message format
		timeString 	= time.strftime( self.__timeFormat, time.localtime())
		hashStr		= '%x' % random.randint(1,4294967295)

		logMessage 	= "%s [%s] %s: %s [%s] {%s}\n" % (timeString, os.getpid(), logInfo, msg, hashStr, stackInfo)

		# file descriptor
		if self.__fd:
			self.__fd.write( logMessage )
			if self.__flush:
				sys.__fd.flush()

		# stderr
		if self.__stderr:
			sys.stderr.write( logMessage )
			if self.__flush:
				sys.stderr.flush()
			
		# logentries
		if self.__logEntries:
			self.__le( msg=msg, mask=mask )
			
		return { 'hash':hashStr }


	# ---


	def fatal( self, msg, params={}, offset=0, depth=0, color='', maxLen=0, level=4 ):
		return self.ni( msg=msg, params=params, offset=offset, depth=depth, color=color, maxLen=maxLen, FATAL=level )

	def error( self, msg, params={}, offset=0, depth=0, color='', maxLen=0, level=4 ):
		return self.ni( msg=msg, params=params, offset=offset, depth=depth, color=color, maxLen=maxLen, ERR=level )

	def warn( self, msg, params={}, offset=0, depth=0, color='', maxLen=0, level=4 ):
		return self.ni( msg=msg, params=params, offset=offset, depth=depth, color=color, maxLen=maxLen, WARN=level )

	def info( self, msg, params={}, offset=0, depth=0, color='', maxLen=0, level=4 ):
		return self.ni( msg=msg, params=params, offset=offset, depth=depth, color=color, maxLen=maxLen, INFO=level )

	def debug( self, msg, params={}, offset=0, depth=0, color='', maxLen=0, level=4 ):
		return self.ni( msg=msg, params=params, offset=offset, depth=depth, color=color, maxLen=maxLen, DEBUG=level )

	# alias
	critical= fatal
	warning	= warn
	err	= error


log = LogNI()


if __name__ == '__main__':

	log.mask( 'ALL' )
	log.stderr( 1 )

	# https://logentries.com
	log.logentries( '<YOUR_LOGENTRIES_KEY>' )
	
	log.ni(    'tests %s %s', (11, 22), INFO=3 )

	log.critical( 'critical test ' )
	log.error( 'error test %s', {'a':1, 'b':2, 'c':3}, level=3 )
	log.warn(  'warning test %s', {'a':1, 'b':2, 'c':3}, level=1 )
	log.info(  'info test %s', {'a':1, 'b':2, 'c':3}, level=1 )
	log.debug( 'debug test %s', time.time(), level=1 )

