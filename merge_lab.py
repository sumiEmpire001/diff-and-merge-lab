"""Inspect text diffs and perform conservative three-way line merges."""
import argparse
import difflib
import json
from pathlib import Path


def diff(before,after,fromfile="before",tofile="after"):
    return "".join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile=fromfile,tofile=tofile))


def changes(base,version):
    matcher=difflib.SequenceMatcher(a=base,b=version,autojunk=False)
    return [(i1,i2,version[j1:j2]) for tag,i1,i2,j1,j2 in matcher.get_opcodes() if tag!="equal"]


def merge(base,ours,theirs):
    if ours==theirs: return {"text":ours,"conflicts":0}
    if ours==base: return {"text":theirs,"conflicts":0}
    if theirs==base: return {"text":ours,"conflicts":0}
    base_lines=base.splitlines(keepends=True)
    a=changes(base_lines,ours.splitlines(keepends=True))
    b=changes(base_lines,theirs.splitlines(keepends=True))
    combined=[]
    conflicts=0
    used_b=set()
    for start,end,replacement in a:
        overlaps=[(j,other) for j,other in enumerate(b) if not (end<=other[0] or other[1]<=start) or (start==end==other[0]==other[1])]
        if overlaps:
            if len(overlaps)==1 and overlaps[0][1]==(start,end,replacement):
                used_b.add(overlaps[0][0])
            else:
                conflicts+=1
                return {"text":None,"conflicts":conflicts}
        combined.append((start,end,replacement))
    combined.extend(change for index,change in enumerate(b) if index not in used_b and all(end<=change[0] or change[1]<=start for start,end,_ in a))
    if len(combined)<len(a)+len(b)-len(used_b):
        return {"text":None,"conflicts":1}
    output=list(base_lines)
    for start,end,replacement in sorted(combined,key=lambda item:(item[0],item[1]),reverse=True):
        output[start:end]=replacement
    return {"text":"".join(output),"conflicts":0}


def main():
    parser=argparse.ArgumentParser(description="Text diff and conservative merge demo")
    sub=parser.add_subparsers(dest="command",required=True)
    d=sub.add_parser("diff")
    d.add_argument("before")
    d.add_argument("after")
    m=sub.add_parser("merge")
    m.add_argument("base")
    m.add_argument("ours")
    m.add_argument("theirs")
    args=parser.parse_args()
    if args.command=="diff":
        print(diff(Path(args.before).read_text(),Path(args.after).read_text()),end="")
        return 0
    result=merge(*(Path(getattr(args,key)).read_text() for key in ("base","ours","theirs")))
    print(json.dumps(result,indent=2))
    return 1 if result["conflicts"] else 0


if __name__=="__main__":
    raise SystemExit(main())
