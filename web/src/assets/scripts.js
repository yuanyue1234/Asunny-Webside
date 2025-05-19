/*
 * @Author: Asunny 91106482+yuanyue1234@users.noreply.github.com
 * @Date: 2024-11-04 14:13:33
 * @LastEditors: Asunny 91106482+yuanyue1234@users.noreply.github.com
 * @LastEditTime: 2025-04-10 23:55:25
 * @FilePath: \yuanyue1234.github.io\scripts.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */

document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    generateTOC();
});

// 切换主题初始化函数
function initTheme() {
    const themeToggle = document.querySelector('.theme-toggle');
    const icon = themeToggle.querySelector('i');
    
    // 检查本地存储中的主题设置
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-theme');
        icon.textContent = 'dark_mode';
    } else {
        document.body.classList.remove('dark-theme');
        icon.textContent = 'light_mode';
    }
    
    // 切换主题
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        const isDark = document.body.classList.contains('dark-theme');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        icon.textContent = isDark ? 'dark_mode' : 'light_mode';
    });
}

// 添加TOC侧边栏目录
function generateTOC() {
    const toc = document.getElementById('toc');
    const headings = document.querySelectorAll('h2, h3');
    const tocLinks = [];

    headings.forEach(heading => {
        if (!heading.id) {
            heading.id = heading.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-');
        }
        
        const link = document.createElement('a');
        link.href = `#${heading.id}`;
        link.textContent = heading.textContent;
        
        if (heading.tagName === 'H3') {
            link.classList.add('h3-link');
        }
        
        link.addEventListener('click', (e) => {
            e.preventDefault();
            heading.scrollIntoView({ behavior: 'smooth' });
            // 更新 URL，但不触发滚动
            history.pushState(null, '', link.href);
        });
        
        toc.appendChild(link);
        tocLinks.push({
            link: link,
            heading: heading
        });
    });

    // 添加滚动监听
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                highlightCurrentSection(tocLinks);
                ticking = false;
            });
            ticking = true;
        }
    });

    // 初始检查 URL 中的锚点
    if (window.location.hash) {
        const targetHeading = document.querySelector(window.location.hash);
        if (targetHeading) {
            setTimeout(() => {
                targetHeading.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        }
    }
}
