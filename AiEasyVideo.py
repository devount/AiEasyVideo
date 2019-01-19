# -*- coding: utf-8 -*-
# The code used download NetEasy Public Lesson video
import os, wget, bs4, requests, re, sys, platform
def _sysexit():
    input("请按回车键退出: ")
    sys.exit()
'''
网页请求处理
'''
def _httpreq(url):
    try:
        req = requests.get(url)
        #req.encoding = 'utf-8'
        return req.text
    except:
        print ('请确保网络连接正常及网址正确！')
        _sysexit()
print ('#'.center(30, '#'))
print ('本程序适用于下载网易公开课视频\n原作者：chiloy@chiloy.com\n多集下载由devount@qq.com增加\n如有问题与建议，请与我联系！')
print ('#'.center(30, '#'))
inputurl = input('请输入或复制(ctrl+v)网易云课堂公开课专辑目录网址：')
reqcontent = bs4.BeautifulSoup(_httpreq(inputurl),"html5lib")
print ('开始抓取页面视频'.center(60, '#'))
print (('课程信息：%s ' % reqcontent.title.string).center(70, '*'))
splitname = reqcontent.title.string.split('：')
idlist2 = reqcontent.find_all(id ="list2")
urlarr = []
lesarr = []
downurlarr = []
for line in idlist2:
    for row in line.find_all(href=re.compile("open.163.com/movie")):
        urlarr.append (row.get('href'))
        lesarr.append (row.next_element)
for lesname in lesarr:
    print ('第%d集：%s' % (lesarr.index(lesname) + 1, lesname))
print ('成功抓取页面视频'.center(60, '#'))
print ('开始生成视频下载链接'.center(60, '#'))
for index in range(len(urlarr)):
    getdowncontent = _httpreq(urlarr[index])
    m3u8flag = getdowncontent.find('-list.m3u8')
    headappsrc = getdowncontent.find("appsrc : '")
    if (m3u8flag == -1):
        tailappsrc = getdowncontent.find('.m3u8') 
    else:
        tailappsrc = m3u8flag
    downurl = getdowncontent[headappsrc +10 :tailappsrc] + '.mp4'
    downurlarr.append(downurl)
    while (len(downurlarr) == len(urlarr)):
        print ('成功生成视频下载链接')
        break

# 创建保存视频的文件夹，并对操作系统做判断
savepath = None
if (platform.system() =="Windows"):
    savepath = "D:\\AiEasyVideo\\" + splitname[0].strip() + '\\' + splitname[1].strip()
    if(os.path.exists(savepath) == False):
            os.makedirs(savepath)
    savepath = savepath + "\\"
elif (platform.system() =="Linux"):
    savepath = '/home/Downloads/AiEasyVideo'
    if (os.path.exists(savepath) == False):
            os.makedirs(savepath)
    savepath = savepath +"/"


print("使用方法如下：".center(60,"#"))
print('默认保存于D:\AiEasyVideo\目录下（如不存在，会自动创建），请保证D盘有足够的硬盘空间！')
print('如下载全部视频，请输入 Y\n间隔单集请用英文逗号","隔开，如"2,3,4"\n连续集数下载请使用"-"表示首尾集数编号，如"2-6"\n支持混合输入，如"2,3,5-8"')
# 手动输入下载集数编号，使用Input采集输入
getinput= input ('请输入你要下载的视频集数编号：')
# 将输入格式化为列表，便于后续处理
downmode = getinput.split(",")

# 判断用户输入的集数编号命令，决定如何下载视频
if (getinput == 'Y'):#遍历下载链接，下载所有视频
    for downstep in downurlarr:	
        print ('\n正在下载第%d集：%s，剩余下载%d集\n' % (downurlarr.index(downstep) + 1, lesarr[downurlarr.index(downstep)], len(downurlarr) - (downurlarr.index(downstep) + 1)))
        videonum= downurlarr.index(downstep) + 1
        savename = savepath + "第%s集-"%videonum +lesarr[downurlarr.index(downstep)] + '.mp4'            
        if(os.path.exists(savename) == False):                 
            wget.download(downstep, savename)
        else:
            print("\n第%d集已存在,将下载下一集！"%(downurlarr.index(downstep) + 1))        
    print ('\n视频下载完成！好好学习！天天向上！')
else:    
    for downindex in downmode:
        if("-" in downindex): #连续下载
            start,end = downindex.split("-")            
            try:
                start,end = int(start),int(end)
            except ValueError:
                print('\n下载编号中除","和"-"外不可出现其他字符，异常编号是%s' % downindex)
                continue
            for downnode in range(start,end+1):#取出下载编号的范围，遍历下载
                try:
                    downnumber = int(downnode)-1
                    if(0 < int(downnode) <=len(downurlarr)):#判断下载的集数是否存在
                        print ('\n正在下载第%d集：%s,请稍后' % (int(downnode), lesarr[downnumber]))
                        videonum= int(downnode)
                        savename = savepath + "第%s集-"%videonum + lesarr[downnumber] +'.mp4'            
                        if(os.path.exists(savename) == False):                 
                            wget.download(downurlarr[downnumber], savename)
                        else:
                            print("\n第%d集已存在,将下载下一集！"%int(downnode))
                    else:
                        print("\n第%d集不存在,将下载下一集"%int(downnode))        
                except KeyboardInterrupt:
                    print("   取消下载该视频")
                    continue
        else:
            try:
                downnumber = int(downindex)-1
                if(0 < int(downindex) <=len(downurlarr)):
                    print ('\n正在下载第%d集：%s,请稍后' % (int(downindex), lesarr[downnumber]))
                    videonum= int(downindex)
                    savename = savepath + "第%s集-"%videonum + lesarr[downnumber] +'.mp4'
                    if(os.path.exists(savename) == False):                 
                        wget.download(downurlarr[downnumber], savename)
                    else:
                        print("\n第%d集已存在,将下载下一集！"%int(downindex))
                else:
                    print("\n第%d集不存在,将下载下一集！"%int(downindex))
            except ValueError:
                print('\n下载编号中除","和"-"外不可出现其他字符，异常编号是%s'% downindex)
                continue
            except KeyboardInterrupt:
                print("   取消下载该视频")
                continue        
    print ('\n视频下载完成！好好学习！天天向上！'.center(50,"#"))
inexit = input ('输入Q退出本程序')
while inexit =='Q':
    print ('感谢使用本程序')
    sys.exit()