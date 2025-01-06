# -*- coding: utf-8 -*-
"""
gitからソースコードを取得

params
    workDir:clone先のディレクトリ
    url:リポジトリのurl
    hash:commit hash値
    dirName:cloneしたリポジトリのディレクトリ名
            未指定の場合はリポジトリと同じ名前
"""

import argparse
import os
import shutil
import git


class srcGetter:
    class RetCode:
        OK = 0
        ERR_CLONE = -1
        ERR_CHKOUT = -2
        ERR_BRANCH = -3
        ERR_ADD = -4
        ERR_COMMIT = -5
        ERR_PUSH = -6
    
    workDir = ''
    url = ''
    hash = ''
    new_branch = ''
    add = ''
    commit_message = ''
    repo = None


    def __init__(this,workDir,url,hash,new_branch,add,commit_message,dirName=None):
        if dirName != None:
            this.workDir = os.path.join(workDir,dirName)
        else:
            this.workDir = os.path.join(workDir,os.path.basename(url).replace(".git", ""))
        this.url = url
        this.hash = hash
        this.new_branch = new_branch
        this.add = add
        this.commit_message = commit_message
        print(this.workDir)


    # clone実行関数
    def clone(this):
        if os.path.exists(this.workDir):
            this.setPermission(0o777)
            shutil.rmtree(this.workDir)

        try:
            os.mkdir(this.workDir)
            print("exec git clone... url=" + this.url)
            this.repo = git.Repo.clone_from(this.url, this.workDir)
            print("Done.")
        except Exception as e:
            print("git clone failed")
            print(e)
            return this.RetCode.ERR_CLONE
        
        return this.RetCode.OK
    

    # hashで指定したcommitにcheckoutする関数
    def checkout(this):
        try:
            print("exec git checkout hash=" + this.hash)
            this.repo.git.checkout(this.hash)
            print("Done.")
        except Exception as e:
            print("git checkout failed")
            print(e)
            return this.RetCode.ERR_CHKOUT
        
        return this.RetCode.OK
    

    # cloneしたディレクトリ内部のpermission変更
    def setPermission(this,flg):
        if os.path.exists(this.workDir):
            for root, dirs, files in os.walk(this.workDir):
                for file in files:
                    os.chmod(os.path.join(root,file),flg)
    
    # ブランチ作成
    def create_branch(this):
        try:
            print("exec git checkout -b " + this.new_branch)
            this.repo.git.checkout('-b', this.new_branch)
            print("Done.")
        except Exception as e:
            print("git branch creation failed")
            print(e)
            return this.RetCode.ERR_BRANCH
        
        return this.RetCode.OK
    
    # ステージング
    def add_files(this):
        try:
            print("exec git add .")
            this.repo.git.add(A=True)
            print("Done.")
        except Exception as e:
            print("git add failed")
            print(e)
            return this.RetCode.ERR_ADD
        
        return this.RetCode.OK
    
    # コミット
    def commit(this):
        try:
            print("exec git commit -m " + this.commit_message)
            this.repo.index.commit(this.commit_message)
            print("Done.")
        except Exception as e:
            print("git commit failed")
            print(e)
            return this.RetCode.ERR_COMMIT
        
        return this.RetCode.OK
    
    # プッシュ
    def push(this):
        try:
            print("exec git push -u origin " + this.new_branch)
            this.repo.git.push('--set-upstream', 'origin', this.new_branch)
            print("Done.")
        except Exception as e:
            print("git push failed")
            print(e)
            return this.RetCode.ERR_PUSH
        
        return this.RetCode.OK
    

    # clone下リポジトリのパスを取得
    def getPath(this):
        return this.workDir
    

    # cloneとexecを実行
    def get(this):
        ret = this.clone()
        if ret != this.RetCode.OK:
            return ret
        
        ret = this.checkout()
        if ret != this.RetCode.OK:
            return ret
        
        ret = this.create_branch()
        if ret != this.RetCode.OK:
            return ret
        
        ret = this.add_files()
        if ret != this.RetCode.OK:
            return ret
        
        ret = this.commit()
        if ret != this.RetCode.OK:
            return ret
        
        ret = this.push()
        if ret != this.RetCode.OK:
            return ret
        
        return ret
    
def main(args):
    if args.dirName != None:
        sg = srcGetter(args.workDir,args.url,args.hash,args.new_branch,args.add,args.commit_message,args.dirName)
    else:
        sg = srcGetter(args.workDir,args.url,args.hash,args.new_branch,args.add,args.commit_message)

    sg.get()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--workDir', default=False,help="作業ディレクトリ",required=True)
    parser.add_argument('--url', default=False,help="gitリポジトリ",required=True)
    parser.add_argument('--hash', default=False,help="対象のhash値",required=True)
    parser.add_argument('--new_branch', default=False,help="新しいブランチ名",required=True)
    parser.add_argument('--add', default=False,help="ステージングするファイル",required=True)
    parser.add_argument('--commit_message', default=False,help="コミットメッセージ",required=True)
    parser.add_argument('--dirName', default=False,help="clone対象を格納するディレクトリ名",required=True)

    args = parser.parse_args()
    ret = main(args)

    exit(ret)