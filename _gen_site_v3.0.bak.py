# 官网 v3 生成脚本（2026-09-30）：在 v2 六页正式站基础上
# 1) 加动效层（天空云层/飘字/滚动显现/数字滚动/截图倾斜/页面过渡等，见 style.css 与 anim.js）
# 2) 公司信息精简：去掉统一社会信用代码与门牌级地址，只写到区县；不写股东结构
# 输出到本目录。运行：python3 _gen_site.py
import os, re, html as H

OUT = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(os.path.dirname(OUT), 'site_v2_2026-09-27')

CO_CN = "西安浠佑拾光电商有限公司"
CO_EN = "XI'AN XIYOU SHIGUANG E-COMMERCE CO., LTD."
LOC_CN = "陕西省西安市浐灞生态区"
LOC_EN = "Chanba Ecological District, Xi'an, Shaanxi, China"
MAIL = "dev@xiyoushiguang.com"

NAV = [('home', 'index.html', '首页'), ('about', 'about.html', '关于我们'), ('product', 'product.html', '产品'),
       ('support', 'support.html', '支持与联系'), ('privacy', 'privacy.html', '隐私政策')]

CLOUD_DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
              '<linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/>'
              '<stop offset="1" stop-color="#e3eefc"/></linearGradient>'
              '<symbol id="cloud"><path fill="url(#cg)" d="M34 82C14 82 4 70 6 57c2-12 12-18 24-17 1-17 16-28 32-25 '
              '7-12 22-19 38-15 13 3 22 13 25 25 12-7 30-3 37 10 3 5 4 9 4 13 15 1 26 12 25 25-1 6-6 9-12 9z"/></symbol>'
              '</defs></svg>')

# (top, width, opacity, duration, delay, static-x)
FAR = [('6%', '140px', '.55', '150s', '-20s', '12%'), ('24%', '100px', '.45', '180s', '-95s', '74%'),
       ('58%', '120px', '.40', '160s', '-60s', '42%'), ('38%', '86px', '.35', '200s', '-150s', '90%')]
NEAR = [('12%', '250px', '.92', '95s', '-12s', '60%'), ('50%', '190px', '.82', '115s', '-58s', '6%'),
        ('68%', '290px', '.72', '105s', '-84s', '30%')]
TWINKLES = [('18%', '20%', '14px', '4.2s', '-1s'), ('64%', '14%', '10px', '3.6s', '-2.4s'), ('82%', '42%', '12px', '5s', '-.6s'),
            ('36%', '8%', '9px', '3.2s', '-1.8s'), ('92%', '70%', '11px', '4.6s', '-3s'), ('8%', '62%', '10px', '3.9s', '-2s')]


def clouds(spec):
    return ''.join(f'<svg class="cl" viewBox="0 -6 200 90" style="--y:{y};--w:{w};--o:{o};--t:{t};--dl:{dl};--x:{x}">'
                   f'<use href="#cloud"/></svg>' for y, w, o, t, dl, x in spec)


def sky_layer():
    tw = ''.join(f'<span class="tw" style="--x:{x};--y:{y};--s:{s};--t:{t};--dl:{dl}">✦</span>' for x, y, s, t, dl in TWINKLES)
    return (f'<div class="sky-layer" aria-hidden="true"><div class="sun"></div>'
            f'<div class="depth" data-k="0.18">{clouds(FAR)}{tw}</div>'
            f'<div class="depth" data-k="0.42">{clouds(NEAR)}</div></div>')


def page_head(title, lead, chars):
    return (f'<div class="hero sky page-head" data-chars="{chars}">{sky_layer()}<div class="wrap">'
            f'<h1 class="enter">{title}</h1><p class="lead enter" style="--d:.12s">{lead}</p></div></div>')


def page(title, active, body, desc):
    nav = ''.join(f'<a href="{h}"{" class=on" if k == active else ""}>{t}</a>' for k, h, t in NAV)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#e6f0ff">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="stylesheet" href="style.css">
<script>(function(d){{if(window.matchMedia&&!matchMedia('(prefers-reduced-motion: reduce)').matches){{d.classList.add('mo');setTimeout(function(){{if(!window.__mo)d.classList.remove('mo')}},2500)}}}})(document.documentElement)</script>
<script src="anim.js" defer></script>
</head>
<body>
{CLOUD_DEFS}
<header class="top" id="top"><div class="wrap">
<a class="brand" href="index.html"><img src="assets/icon.png" alt="浠佑拾光"><span>浠佑拾光</span></a>
<nav>{nav}</nav>
</div><div class="progress" aria-hidden="true"></div></header>
{body}
<footer><div class="wrap">
<div class="cols">
<div><h4>{CO_CN}</h4><div class="en">{CO_EN}</div>
<div>{LOC_CN} · <span class="en">Xi'an, Shaanxi, China</span></div>
<div>联系邮箱：<a href="mailto:{MAIL}" style="display:inline">{MAIL}</a></div></div>
<div><h4>公司</h4><a href="about.html">关于我们</a><a href="about.html#en">Company Profile (EN)</a><a href="support.html#contact">联系我们</a></div>
<div><h4>产品与法律</h4><a href="product.html">云上识字乐园</a><a href="support.html">帮助与常见问题</a><a href="terms.html">用户协议</a><a href="privacy.html">隐私政策</a></div>
</div>
<div class="copy">© 2026 {CO_CN} · {CO_EN} · 保留所有权利</div>
</div></footer>
<a class="totop" href="#top" aria-label="回到顶部">↑</a>
</body>
</html>
'''


pages = {}

PLANE = ('<div class="mail-fx" aria-hidden="true">'
         '<svg class="trail" viewBox="0 0 330 140" preserveAspectRatio="none"><path d="M6 128 C 90 130, 120 40, 200 66 S 290 70, 300 22" '
         'fill="none" stroke="#a9c2ef" stroke-width="2" stroke-linecap="round"/></svg>'
         '<svg class="plane" viewBox="0 0 64 64"><path d="M4 30 L60 6 L44 58 L32 38 Z" fill="#fff" stroke="#2d6cdf" stroke-width="2.5" stroke-linejoin="round"/>'
         '<path d="M60 6 L32 38" stroke="#2d6cdf" stroke-width="2.5"/>'
         '<path d="M32 38 L28 52 L38 44" fill="#d6e4ff" stroke="#2d6cdf" stroke-width="2.5" stroke-linejoin="round"/></svg></div>')

pages['index.html'] = page('浠佑拾光 · 儿童启蒙内容与软件研发', 'home', f'''
<div class="hero sky" data-chars="云 字 山 水 日 月 花 鸟 天 人 火 木">{sky_layer()}<div class="wrap">
<h1 class="enter">用心做<span class="grad">温暖的儿童启蒙内容</span></h1>
<p class="lead enter" style="--d:.14s">浠佑拾光是一家位于西安的小微团队，专注 4–6 岁儿童的启蒙内容与软件研发。第一件作品《云上识字乐园》正在家庭内测中，计划于 2026 年底登陆 App Store。</p>
<div class="enter" style="--d:.28s"><a class="btn" href="product.html">了解云上识字乐园</a><a class="btn ghost" href="about.html">关于我们</a></div>
</div></div>
<section><div class="wrap">
<div class="grid g3">
<div class="card rv"><div class="stat"><span class="num" data-to="39">39</span><small>座云屿（学习单元）</small></div></div>
<div class="card rv"><div class="stat"><span class="num" data-to="278">278</span><small>张手工打磨的学习卡</small></div></div>
<div class="card rv"><div class="stat"><span class="num" data-to="23">23</span><small>种轮换登场的小游戏</small></div></div>
</div>
</div></section>
<section class="alt"><div class="wrap">
<div class="split">
<div>
<h2 class="rv">云上识字乐园</h2>
<p class="sub rv">面向 4–6 岁儿童的识字、数学与拼音启蒙 App</p>
<p class="rv">孩子每天只走一小段云上旅程：认识两三个新的字宝宝，认一认、读一读、写一写、玩一玩、测一测，五到八分钟刚刚好。全语音引导、零文字界面，孩子自己就能上手；家长门与使用节制设计，让家长放心把设备交给孩子。</p>
<p class="rv">识字线覆盖 200 余个入学前常用汉字（按 2024 版一年级上册识字表校准），数学线包含数字、图形、合与分、钱币与时钟，拼音线涵盖 23 个声母、24 个韵母与 16 个整体认读音节。</p>
<p class="rv"><a href="product.html">查看产品详情 →</a></p>
</div>
<div class="rv zoom"><div class="shot-wrap"><span class="glow"></span><div class="float"><img class="shot tilt" src="assets/app_home.jpg" alt="云上识字乐园 App 首页截图"></div></div></div>
</div>
</div></section>
<section><div class="wrap">
<h2 class="rv">我们的产品准则</h2>
<p class="sub rv">这三条不是口号，是写进代码里的规则。</p>
<div class="grid g3">
<div class="card rv"><h3>内容厚度优先</h3><p>每一个字、每一张插画、每一句旁白都逐个手工校对。我们相信启蒙产品的差距，藏在第两百次修改里。</p></div>
<div class="card rv"><h3>儿童体验优先</h3><p>不催促、不喧哗、不制造焦虑。孩子在游戏与故事里自然地认识世界，学的就是玩的。</p></div>
<div class="card rv"><h3>家长省心优先</h3><p>无广告、无账号、无第三方 SDK，学习数据只保存在家里的设备上。家长功能入口需算术验证，孩子误触不了。</p></div>
</div>
</div></section>
<section class="alt"><div class="wrap">
<h2 class="rv">孩子们将要唤醒的字精灵</h2>
<p class="sub rv">每个汉字都有一位专属的字精灵插画，认字、读词、玩游戏，都围绕它展开。</p>
<div class="ph kb rv zoom"><img class="img" src="assets/spirits.jpg" alt="云上识字乐园字精灵插画：颜色字一组"></div>
</div></section>
<section class="mail"><div class="wrap">
{PLANE}
<h2 class="rv">写信给云上</h2>
<p class="sub rv">合作、反馈，或者只是打个招呼。</p>
<p class="rv">邮箱：<a href="mailto:{MAIL}">{MAIL}</a>（一般 3 个工作日内回复）<br>更多联系方式与常见问题见 <a href="support.html">支持与联系</a>。</p>
</div></section>
''', "浠佑拾光（西安浠佑拾光电商有限公司）专注儿童启蒙内容与软件研发，首款产品《云上识字乐园》面向 4–6 岁儿童。")

pages['about.html'] = page('关于我们 · 浠佑拾光', 'about', f'''
{page_head('关于浠佑拾光', '一家把「内容厚度」当命根子的小微团队', '拾 光 云 山 水 月')}
<section><div class="wrap">
<div class="split">
<div>
<p class="rv">{CO_CN}成立于 2026 年 5 月，位于陕西省西安市浐灞生态区，由创始团队共同发起，主营两块业务：<b>儿童启蒙内容与软件研发</b>，以及<b>自有品牌的跨境电商业务</b>（家居生活类，面向海外市场）。</p>
<p class="rv">「浠佑拾光」取意「珍惜、守护，拾起每一段光阴」。我们自己也是家长，深知入学前那一两年既珍贵又容易被焦虑填满。所以我们只做一件事：让孩子在不知不觉的快乐里完成入学前的启蒙准备，让家长在一旁安心地看着就好。</p>
<p class="rv">团队目前的全部精力，都放在第一款产品《云上识字乐园》上：从课程包设计、插画与语音，到 App 的每一处交互，都由团队自己一点点打磨。</p>
</div>
<div class="ph rv zoom"><img class="img" src="assets/isle_zi.jpg" alt="云上识字乐园：识字云屿插画"></div>
</div>
</div></section>
<section class="alt"><div class="wrap">
<h2 class="rv">公司信息</h2>
<table class="info rv">
<tr><th>公司名称</th><td>{CO_CN}</td></tr>
<tr><th>英文名称</th><td class="en">{CO_EN}</td></tr>
<tr><th>成立时间</th><td>2026 年 5 月</td></tr>
<tr><th>所在地</th><td>{LOC_CN}</td></tr>
<tr><th>主营业务</th><td>儿童启蒙内容与软件研发；自有品牌跨境电商</td></tr>
<tr><th>官方网站</th><td>https://xiyoushiguang.com</td></tr>
<tr><th>联系邮箱</th><td>{MAIL}</td></tr>
</table>
</div></section>
<section><div class="wrap">
<h2 class="rv">我们走到哪儿了</h2>
<ul class="timeline rv-line">
<li class="rv"><b>2026 年 5 月</b><span>公司在西安注册成立。</span></li>
<li class="rv"><b>2026 年 7 月</b><span>《云上识字乐园》立项，完成首个可玩版本：数据驱动的课件引擎、五座云屿五十个字全插画上线。</span></li>
<li class="rv"><b>2026 年 8 月</b><span>识字线 200 字课程包建成；新增数学启蒙线、字源故事、描红写字工坊、阅读馆与家长周报；家庭内测开始。</span></li>
<li class="rv"><b>2026 年 9 月</b><span>拼音线建成，App 达到 39 座云屿、278 张学习卡、23 种小游戏；公司官网与企业邮箱启用，开始上架前的合规准备。</span></li>
<li class="rv next"><b>2026 年第四季度（计划）</b><span>完成付费与合规准备，登陆 App Store。</span></li>
</ul>
</div></section>
<section class="alt" id="en"><div class="wrap en">
<h2 class="rv">Company Profile</h2>
<p class="rv"><b>{CO_EN}</b> ({CO_CN}) is a small company founded in May 2026 and based in the Chanba Ecological District of Xi'an, Shaanxi, China. We work in two areas: <b>early-learning content and software for children aged 4–6</b>, and <b>a private-label cross-border e-commerce business</b> in home and lifestyle goods for overseas markets.</p>
<p class="rv">Our first product, <b>Cloud Literacy Garden</b> (云上识字乐园), is an iPad and iPhone app that helps pre-school children learn their first 200+ Chinese characters, early maths and pinyin through short daily sessions of illustrated stories, tracing and mini-games. It has no ads, no accounts and no third-party SDKs; all learning data stays on the family's device. The app is currently in family beta testing and is planned for release on the App Store by the end of 2026.</p>
<p class="rv">Location: {LOC_EN}. Contact: <a href="mailto:{MAIL}">{MAIL}</a>.</p>
</div></section>
''', "西安浠佑拾光电商有限公司简介：成立于 2026 年 5 月，主营儿童启蒙内容与软件研发及自有品牌跨境电商。Company profile of Xi'an Xiyou Shiguang E-commerce Co., Ltd.")

pages['product.html'] = page('云上识字乐园 · 浠佑拾光', 'product', f'''
<div class="hero sky" data-chars="字 a o e 1 2 3 山 水 月">{sky_layer()}<div class="wrap">
<div class="split">
<div>
<h1 class="enter"><span class="grad">云上识字乐园</span></h1>
<p class="lead enter" style="--d:.12s">面向 4–6 岁儿童的识字、数学与拼音启蒙 App。每天一小段云上旅程，认、读、写、玩、测五个环节一气呵成。</p>
<p class="note enter" style="--d:.24s">当前状态：家庭内测中 · 支持 iPad 与 iPhone · 计划 2026 年底登陆 App Store</p>
</div>
<div class="enter" style="--d:.2s"><div class="shot-wrap"><span class="glow"></span><div class="float"><img class="shot tilt" src="assets/app_home.jpg" alt="云上识字乐园 App 首页"></div></div></div>
</div>
</div></div>
<section><div class="wrap">
<h2 class="rv">三条学习线</h2>
<p class="sub rv">把入学前最需要的三样东西，做成孩子愿意每天回来的三片云上世界。</p>
<div class="grid g3">
<div class="card rv"><div class="ph"><img class="img" src="assets/isle_zi.jpg" alt="识字云屿"></div><h3>识字线 · 200 余字</h3><p>按 2024 版一年级上册识字表校准的 200 余个常用汉字，分 20 座云屿循序渐进；每个字配专属字精灵插画、词组与例句，另有 27 组形近字专项与「火眼金睛」辨形游戏。</p></div>
<div class="card rv"><div class="ph"><img class="img" src="assets/isle_math.jpg" alt="数学云屿"></div><h3>数学线 · 数与形</h3><p>数字乐园、图形王国、合与分、钱币岛、时间岛：从 1–10 的数量感，到认识图形、元角分与整点时钟，用游戏建立最初的数学直觉。</p></div>
<div class="card rv"><div class="ph"><img class="img" src="assets/isle_fog.jpg" alt="拼音云屿"></div><h3>拼音线 · 63 个音</h3><p>23 个声母、24 个韵母、16 个整体认读音节，配「拼读小火车」游戏；用孩子已经认识的字借音，先会读再会拼。</p></div>
</div>
</div></section>
<section class="alt"><div class="wrap">
<h2 class="rv">五个环节，五到八分钟</h2>
<div class="grid g4">
<div class="card rv"><h3>认</h3><p>字源动画与温柔旁白：看见字的样子，听见字的故事。40 篇「字的故事」从插画、剪影、甲骨文到楷体四幕演变。</p></div>
<div class="card rv"><h3>读</h3><p>词组胶囊逐个点读，例句跟读逐字高亮；阅读馆 30 篇小故事全部只用已学过的字。</p></div>
<div class="card rv"><h3>写</h3><p>描红写字工坊：标准笔顺演示后自由书写，写对亮起金色流光。</p></div>
<div class="card rv"><h3>玩 · 测</h3><p>捉字泡泡、图字配对、组词工坊、句子小火车等 23 种小游戏轮换登场；听音选字小关卡配合复习曲线，学过的字宝宝不走丢。</p></div>
</div>
</div></section>
<section><div class="wrap">
<div class="split">
<div>
<h2 class="rv">为家长做的设计</h2>
<ul class="perks">
<li class="rv"><b>家长门：</b>家长功能入口需算术验证，孩子误触不了设置与统计页。</li>
<li class="rv"><b>使用节制：</b>内置每日学习节奏、20 分钟护眼提醒，玩够了，月亮会请字宝宝们去睡觉。</li>
<li class="rv"><b>家长周报与薄弱字追踪：</b>一周学了什么、哪些字需要复习、亲子任务建议，一页看清。</li>
<li class="rv"><b>多娃档案：</b>一台设备可为家里多个孩子分别建立学习档案。</li>
<li class="rv"><b>成就系统：</b>星星罐、打卡链、13 枚徽章与可打印的岛主证书。</li>
</ul>
</div>
<div class="ph kb rv zoom"><img class="img" src="assets/spirits.jpg" alt="字精灵插画"></div>
</div>
</div></section>
<section class="alt"><div class="wrap">
<h2 class="rv">儿童安全与隐私</h2>
<div class="grid g4">
<div class="card rv"><h3>无广告</h3><p>没有任何形式的广告，也没有诱导分享、诱导付费的设计。</p></div>
<div class="card rv"><h3>无账号</h3><p>不需要注册、登录，不要求提供任何个人信息。</p></div>
<div class="card rv"><h3>数据仅存本地</h3><p>学习记录只保存在您的设备上，不上传任何服务器，卸载即彻底删除。</p></div>
<div class="card rv"><h3>无第三方 SDK</h3><p>不接入统计、推送或广告类 SDK；语音朗读使用系统本地能力，不联网、不录音。</p></div>
</div>
<p class="rv" style="margin-top:18px">完整说明见 <a href="privacy.html">《隐私政策》</a>。</p>
</div></section>
<section><div class="wrap">
<h2 class="rv">字精灵长这样</h2>
<p class="sub rv">每个汉字都有一位专属插画角色，认字、读词、玩游戏，都围绕它展开。</p>
<div class="grid g3">
<div class="card rv"><div class="ph"><img class="img" src="assets/zi_mao.jpg" alt="猫字精灵"></div><p style="text-align:center;margin-top:8px">猫 māo</p></div>
<div class="card rv"><div class="ph"><img class="img" src="assets/zi_gou.jpg" alt="狗字精灵"></div><p style="text-align:center;margin-top:8px">狗 gǒu</p></div>
<div class="card rv"><div class="ph"><img class="img" src="assets/zi_ma.jpg" alt="马字精灵"></div><p style="text-align:center;margin-top:8px">马 mǎ</p></div>
</div>
</div></section>
<section class="alt"><div class="wrap">
<h2 class="rv">价格与获取方式</h2>
<p class="rv">《云上识字乐园》将通过 App Store 发行，计划采用<b>一次性买断、无订阅、无广告</b>的方式：前几座云屿免费体验，满意后一次付费解锁全部内容。具体价格将在上架时公布。想第一时间收到上架通知，欢迎发邮件至 <a href="mailto:{MAIL}">{MAIL}</a>。</p>
</div></section>
''', "云上识字乐园：面向 4–6 岁儿童的识字、数学与拼音启蒙 App，39 座云屿、278 张学习卡、23 种小游戏，无广告、无账号、数据仅存本地。")

pages['support.html'] = page('支持与联系 · 浠佑拾光', 'support', f'''
{page_head('支持与联系', '关于产品、合作或隐私的任何问题，都欢迎写信给我们。', '信 云 问 答 你 好')}
<section><div class="wrap">
<div class="grid g2" id="contact">
<div class="card rv"><h3>联系方式</h3>
<p><b>邮箱：</b><a href="mailto:{MAIL}">{MAIL}</a></p>
<p><b>回复时间：</b>一般问题 3 个工作日内回复；涉及隐私与个人信息的问题 15 个工作日内答复。</p>
<p><b>工作时间：</b>周一至周五 9:00–18:00（北京时间）</p>
</div>
<div class="card rv"><h3>公司信息</h3>
<p>{CO_CN}</p>
<p class="en">{CO_EN}</p>
<p>所在地：{LOC_CN} · <span class="en">Xi'an, Shaanxi, China</span></p>
<p>如需寄送资料或样品，请先发邮件联系，我们会回复收件地址。</p>
</div>
</div>
</div></section>
<section class="alt"><div class="wrap faq">
<h2 class="rv">常见问题</h2>
<details class="rv" open><summary>云上识字乐园现在能下载吗？</summary><p>还不能。App 目前处于家庭内测阶段，计划 2026 年底通过 App Store 正式发布。留下邮箱，我们会在上架时通知你。</p></details>
<details class="rv"><summary>支持哪些设备？</summary><p>iPad 与 iPhone（iOS / iPadOS 17 及以上）。iPad 大屏体验最佳，描红写字工坊建议搭配手指或触控笔使用。</p></details>
<details class="rv"><summary>适合多大的孩子？</summary><p>主要面向 4–6 岁、入学前一两年的孩子。界面零文字、全语音引导，孩子可以独立操作；家长功能需算术验证进入。</p></details>
<details class="rv"><summary>需要注册账号吗？会收集孩子的信息吗？</summary><p>不需要账号，也不收集任何个人信息。全部学习数据只保存在您的设备本地，不上传服务器，卸载即彻底删除。详见 <a href="privacy.html">《隐私政策》</a>。</p></details>
<details class="rv"><summary>有广告或内购陷阱吗？</summary><p>没有广告，没有诱导分享或诱导付费设计。付费方式计划为一次性买断、无订阅，前几座云屿免费体验。</p></details>
<details class="rv"><summary>换了设备，学习进度能转移吗？</summary><p>当前版本数据仅存本地，可通过家长页的「档案导出」功能导出，再在新设备上导入。如未来加入云端备份，我们会在功能上线前更新隐私政策并征得监护人同意。</p></details>
<details class="rv"><summary>如何申请退款？</summary><p>App Store 内的购买由 Apple 处理，可在 reportaproblem.apple.com 提交退款申请。遇到困难也可以写信给我们，我们会协助处理。</p></details>
<details class="rv"><summary>可以合作或投稿内容吗？</summary><p>欢迎插画、配音、幼教内容方面的合作，请发邮件至 {MAIL} 并附作品或简介。</p></details>
</div></section>
''', "浠佑拾光支持与联系：联系邮箱、公司信息与云上识字乐园常见问题。")

# 用户协议、隐私政策：正文沿用 v2，只换外壳；阅读页不加天空，只做整页淡入与阅读进度条
def v2_doc(name):
    h = open(os.path.join(V2, name), encoding='utf-8').read()
    m = re.search(r'<section><div class="wrap doc">(.*?)</div></section>\s*<footer>', h, re.S)
    assert m, name
    return m.group(1)

pages['terms.html'] = page('用户协议 · 云上识字乐园', 'terms',
                           f'<section><div class="wrap doc rv">{v2_doc("terms.html")}</div></section>',
                           "《云上识字乐园》用户协议：服务内容、儿童使用、付费与退款、知识产权、隐私与免责条款。")
pages['privacy.html'] = page('隐私政策 · 云上识字乐园', 'privacy',
                             f'<section><div class="wrap doc rv">{v2_doc("privacy.html")}</div></section>',
                             "《云上识字乐园》隐私政策：零收集原则，无账号、不收集个人信息、学习数据仅存设备本地。")

pages['404.html'] = page('页面未找到 · 浠佑拾光', '',
                         page_head('这朵云飘走了', '你要找的页面不存在或已移动。', '云 ? 找 路') +
                         '<section><div class="wrap"><p><a class="btn" href="index.html">回到首页</a></p></div></section>',
                         '页面未找到')

for k, v in pages.items():
    open(os.path.join(OUT, k), 'w', encoding='utf-8').write(v)

open(os.path.join(OUT, 'robots.txt'), 'w').write("User-agent: *\nAllow: /\nSitemap: https://xiyoushiguang.com/sitemap.xml\n")
urls = ['', 'about.html', 'product.html', 'support.html', 'terms.html', 'privacy.html']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>https://xiyoushiguang.com/{u}</loc><lastmod>2026-09-30</lastmod></url>\n' for u in urls) + '</urlset>\n')

for k in pages:
    h = open(os.path.join(OUT, k), encoding='utf-8').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<svg.*?</svg>', '', h, flags=re.S)
    t = H.unescape(re.sub(r'<[^>]+>', ' ', t)); t = re.sub(r'\s+', ' ', t)
    print(f'{k}: {len(t)} visible chars')
