# -*- coding: utf-8 -*-
import sys
import string
from burp import IBurpExtender, IContextMenuFactory, IContextMenuInvocation
from java.util import ArrayList
from javax.swing import JMenuItem


class BurpExtender(IBurpExtender, IContextMenuFactory):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        sys.stdout = callbacks.getStdout()
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("JavaScript EncodeAs")
        callbacks.registerContextMenuFactory(self)
        print("JavaScript EncodeAs - v1.0")
        print("by Jayden Caelli (@ret2desync)")
        print("")
        print("The documentation can be found at https://github.com/ret2desync/JavaScript-EncodeAs-Burp-Plugin")

    def createMenuItems(self, invocation):
        self.context = invocation
        if invocation.getInvocationContext() in [IContextMenuInvocation.CONTEXT_MESSAGE_EDITOR_REQUEST, IContextMenuInvocation.CONTEXT_MESSAGE_EDITOR_RESPONSE]:
            bounds = self.context.getSelectionBounds()
            start, end = bounds[0], bounds[1]
            if end - start == 0:
                enable_menu_items = False
            else:
                enable_menu_items = True
            return self.create_menu_list(enable=enable_menu_items)
       
    def create_menu_list(self, enable):
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Unicode Encode Non-Alpha (\\u0061abcd)", enabled=enable, actionPerformed=self.encode_unicode_non_alpha))
        menu_list.add(JMenuItem("Unicode Encode All Characters (\\u0061)", enabled=enable,actionPerformed=self.encode_unicode_all))
        menu_list.add(JMenuItem("Unicode Aware Encode Non-Alpha (\\u{61}abcd)", enabled=enable,actionPerformed=self.encode_unicode_aware_non_alpha))
        menu_list.add(JMenuItem("Unicode Aware Encode All Characters (\\u{61})", enabled=enable,actionPerformed=self.encode_unicode_aware_all))
        menu_list.add(JMenuItem("Hex Encode Non-Alpha (\\x61abcd)", enabled=enable,actionPerformed=self.encode_hex_non_alpha))        
        menu_list.add(JMenuItem("Hex Encode All Characters (\\x61)", enabled=enable, actionPerformed=self.encode_hex_all))
        return menu_list

    def encode_hex(self, event, allChars):
        http_traffic = self.context.getSelectedMessages()
        bounds = self.context.getSelectionBounds()
        start, end = bounds[0], bounds[1]

        for traffic in http_traffic:
            request = traffic.getRequest()
            selectedString = self._helpers.bytesToString(request[start:end])
            encodedString = self.encode_string_hex(selectedString, allChars)
            encodedBytes = self._helpers.stringToBytes(encodedString)
            newRequest = request[:start] + encodedBytes + request[end:]
            traffic.setRequest(newRequest)
                
    def encode_string_hex(self, encode_string, allChars):
        if allChars:
            return ''.join('\\x{:02X}'.format(ord(a)) for a in encode_string)
        else:
            return ''.join('\\x{:02X}'.format(ord(a)) if not a in list(string.ascii_lowercase + string.ascii_uppercase + string.digits) else a for a in encode_string)

    
    def encode_hex_non_alpha(self, event):
        self.encode_hex(event, False)
    
    def encode_hex_all(self, event):
        self.encode_hex(event, True)

    def encode_unicode_aware(self, event, allChars):
        http_traffic = self.context.getSelectedMessages()
        bounds = self.context.getSelectionBounds()
        start, end = bounds[0], bounds[1]

        for traffic in http_traffic:
            request = traffic.getRequest()
            selectedString = self._helpers.bytesToString(request[start:end])
            encodedString = self.encode_string_unicode_aware(selectedString, allChars)
            encodedBytes = self._helpers.stringToBytes(encodedString)
            newRequest = request[:start] + encodedBytes + request[end:]
            traffic.setRequest(newRequest)

    def encode_string_unicode_aware(self, encode_string, allChars):
        if allChars:
            return ''.join('\\u{'+'{}'.format(hex(ord(a)).replace('0x','') + '}') for a in encode_string)
        else:
            return ''.join('\\u{'+'{}'.format(hex(ord(a)).replace('0x','') + '}') if not a in list(string.ascii_lowercase + string.ascii_uppercase + string.digits) else a for a in encode_string)
    
    def encode_unicode_aware_non_alpha(self, event):
        self.encode_unicode_aware(event, False)
    
    def encode_unicode_aware_all(self, event):
        self.encode_unicode_aware(event, True)

    def encode_unicode(self, event, allChars):
        http_traffic = self.context.getSelectedMessages()
        bounds = self.context.getSelectionBounds()
        start, end = bounds[0], bounds[1]

        for traffic in http_traffic:
            request = traffic.getRequest()
            selectedString = self._helpers.bytesToString(request[start:end])
            encodedString = self.encode_string_unicode(selectedString, allChars)
            encodedBytes = self._helpers.stringToBytes(encodedString)
            newRequest = request[:start] + encodedBytes + request[end:]
            traffic.setRequest(newRequest)
                
    def encode_string_unicode(self, encode_string, allChars):
        if allChars:
            return ''.join('\\u{:04X}'.format(ord(a)) for a in encode_string)
        else:
            return ''.join('\\u{:04X}'.format(ord(a)) if not a in list(string.ascii_lowercase + string.ascii_uppercase + string.digits) else a for a in encode_string)
            
    def encode_unicode_non_alpha(self, event):
        self.encode_unicode(event, False)
    
    def encode_unicode_all(self, event):
        self.encode_unicode(event, True)
        