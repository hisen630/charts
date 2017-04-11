#coding: utf-8
import time
import ldap
import json
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8") 


class UserInfoHelper(object):
    __ldappath = "ldap://192.168.100.4:389/";
    FoundResult_ServerBusy = "Server is busy"
    FoundResult_NotFound = "Not Found"

    def __init__(self, name, password):
        self.ldapuser = name;
        self.ldappass = password;

    def searchBase(self, **kargs):
        try:
            l = ldap.initialize(self.__ldappath)
            l.protocol_version = ldap.VERSION3
            l.simple_bind("hillhouse\%s" % self.ldapuser, self.ldappass)
            searchScope  = ldap.SCOPE_SUBTREE

            time.sleep(0.5)
            baseDN = "DC=hillhouse,DC=com,DC=cn"
            searchFilter = '(sAMAccountName=%s)' % self.ldapuser
            retrieveAttributes = ['*']

            if 'path' in kargs:
                baseDN = kargs['path']
            if 'filter' in kargs:
                searchFilter = kargs['filter']
            if 'fields' in kargs:
                retrieveAttributes = kargs['fields']

            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_type, result_data = l.result(ldap_result_id, 0)

            if(not len(result_data) == 0):
                return 1, result_data
            else:
                return 0, self.FoundResult_NotFound
        except ldap.LDAPError, e:
            print e
            return 0, self.FoundResult_ServerBusy
        finally:
            l.unbind()
            del l

    def infoGet(self, trynum = 2):
        i = 0
        isfound = 0
        foundResult = ""
        while(i < trynum):
            isfound, foundResult = self.searchBase()
            if(isfound):
              break
            i+=1
        return isfound, foundResult

def getListMembers(uh, listPath):
    status, info = uh.searchBase(path=listPath, filter='CN=*', fields=["member"])
    res = []
    if status:
        res = info[0][1]['member']
    return res

def getUserInfo(uh, userPath):
    status, info = uh.searchBase(path=userPath, filter='CN=*', fields=["*"])
    return info

if __name__ == '__main__':
    pass
    #get full userinfo
    #userHandle = UserInfoHelper('xzheng', '######password here#######')
    #parts = { 
    #        "bj":"CN=BJ.list,OU=Security Groups,OU=Managed Groups,OU=IT Management,DC=hillhouse,DC=com,DC=cn",
    #        "hk":"CN=HK.list,OU=Security Groups,OU=Managed Groups,OU=IT Management,DC=hillhouse,DC=com,DC=cn",
    #        "sg":"CN=SG.list,OU=Security Groups,OU=Managed Groups,OU=IT Management,DC=hillhouse,DC=com,DC=cn",
    #        "sz":"CN=SZ.list,OU=Security Groups,OU=Managed Groups,OU=IT Management,DC=hillhouse,DC=com,DC=cn",
    #        }
    #allMembers = []
    #for pt in parts:
    #    listMembers = getListMembers(userHandle, parts[pt])
    #    for up in listMembers:
    #        if up not in allMembers:
    #            allMembers.append(up)
    #f = open("/tmp/ureqlist", "w")
    #i = 0
    #for upath in allMembers:
    #    req = str(getUserInfo(userHandle, upath))
    #    f.write(req+"\n")
    #    i+=1
    #    print i
    #f.close()
