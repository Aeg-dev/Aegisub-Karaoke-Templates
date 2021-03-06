from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import pathlib


env = Environment(loader=FileSystemLoader('./template'))
page_head_title   = 'ASS FX Template Viewer'
inf_css_path = '../infinite-scroll-docs.css'
inf_js_path  = '../infinite-scroll-docs.min.js'
page_to_index_url = '../index.html'
index_page_name = 'Main Page / TOP'
page_title = 'ASS FX Flow'


def gen_pages(img_list, idx=2, is_last_page=True):
    global env
    template = env.get_template('page.j2')
    next_page_link = f'html/page{idx + 1}.html'
    
    with open(f"html/page{idx}.html", 'w') as fout:
        html_content = template.render(
            # CSS/JS
            inf_css_path=inf_css_path,
            inf_js_path=inf_js_path,
            # title/section name
            page_head_title=page_head_title,
            page_to_index_url=page_to_index_url,
            index_page_name=index_page_name,
            page_title=page_title,
            # data
            img_list=img_list,
            is_last_page=is_last_page,
            next_page_link=next_page_link,
        )
        fout.write(html_content)


def gen_main_page(img_list, idx=1, is_last_page=True):
    global env
    template = env.get_template('page.j2')
    inf_css_path = 'infinite-scroll-docs.css'
    inf_js_path  = 'infinite-scroll-docs.min.js'
    page_to_index_url = 'index.html'
    next_page_link = f'html/page{idx + 1}.html'
    
    with open("index.html", 'w') as fout:
        html_content = template.render(
            # CSS/JS
            inf_css_path=inf_css_path,
            inf_js_path=inf_js_path,
            # title/section name
            page_head_title=page_head_title,
            page_to_index_url=page_to_index_url,
            index_page_name=index_page_name,
            page_title=page_title,
            # data
            img_list=img_list,
            is_last_page=is_last_page,
            next_page_link=next_page_link,
        )
        fout.write(html_content)


def real_path(path):
    return [ '../_vout/' + p.name for p in path ]

# if __name__ == "__main__":

img_root_path = Path(r'F:\subt\Aegisub-Karaoke-Templates\_vout')
gifs = list(img_root_path.glob('*.gif'))
webps = list(img_root_path.glob('*.webp'))
imgs = gifs

steps = 12
rpath = [ '../_vout/' + p.name for p in imgs[0:steps] ]
gen_main_page(rpath, is_last_page=False)
imgs = imgs[steps:]


total_pages = 100
img_count = 0
for page in range(1, total_pages + 1):
    if page==total_pages or img_count>=len(imgs):
        is_last_page = True 
    else:
        is_last_page = False

    img_list = imgs[ (page*steps) : ((page+1)*steps) ]
    rpath = [ '../../_vout/' + p.name for p in img_list ]
    img_count = img_count + len(rpath)
    gen_pages(rpath, idx=(page+1), is_last_page=is_last_page)

    if is_last_page:
        print(f'总共 {page + 1} 页')
        print(f'总共 {img_count + steps} 张图')
        break
