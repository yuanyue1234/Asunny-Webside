<script setup>
import { ref } from 'vue';
import { Star, Mail, Phone, Award, Briefcase, GraduationCap, Code, Target } from 'lucide-vue-next';

const resumeData = ref({
  name: '袁越',
  title: '软件工程师',
  avatarUrl: 'https://asunny-1314135129.cos.ap-guangzhou.myqcloud.com/img/asunny%E9%BB%91%E8%BE%B9.png',
  contact: {
    email: 'e@asunny.top',
    phone: '166 7677 0259',
  },
  education: {
    school: '常德职业技术学校',
    degree: '大专',
    graduationDate: '预计2026年9月毕业'
  },
  skills: [
    { category: '编程语言', items: ['Python', 'Java', 'JavaScript'] },
    { category: 'Web开发', items: ['Django', 'Vue3', 'jQuery', 'Ajax', 'Bootstrap'] },
    { category: '数据处理', items: ['网络爬虫', '数据可视化'] },
    { category: '系统与工具', items: ['Linux', 'Git', 'MySQL'] },
    { category: '其他技能', items: ['Office办公套件', 'Adobe系列软件（PS, PR, AE）'] }
  ],
  projects: [
    {
      name: '个人博客网站',
      description: [
        'Linux云主机和宝塔面板搭建',
        'Material 3风格设计，现代UI',
        'GitHub提交功能，文章发布系统',
        '个人作品展示栏'
      ]
    },
    {
      name: '豆瓣Top100电影信息爬虫及观影网站',
      description: [
        'Python爬虫抓取豆瓣Top100电影信息',
        '电影信息展示和用户观影记录功能',
        '网站性能优化'
      ]
    },
    {
      name: '其他个人项目',
      description: [
        '个人网盘项目：文件存储和分享',
        'AI反代项目：AI应用在网络服务中的探索',
        '网络代理项目：提高网络访问效率和安全性'
      ]
    }
  ],
  experience: [
    {
      title: '培训机构教师',
      company: '培训机构',
      period: '2024年8月 - 至今',
      responsibilities: [
        '主要教授课程：Scratch3, ScratchJr, Python',
        '开发互动式教学方法，提高学生学习兴趣和效率',
        '建立良好师生关系，获得学生和家长的积极反馈'
      ]
    }
  ],
  achievements: [
    '获得计算机一级证书',
    '校级优秀学生荣誉称号',
    '担任计算机协会会员，组织技术交流活动'
  ],
  personalQualities: [
    '学习能力强，对新技术有高度接受能力',
    '具备出色的问题解决能力和搜索技巧',
    '热爱技术钻研，有丰富的DIY经验',
    '良好的沟通能力和团队协作精神',
    '具有创新思维，善于将AI技术应用到日常工作中'
  ],
  careerObjective: '致力于在AI应用和软件工程领域深耕，期望通过不断学习和实践，成为行业内的佼佼者。目标是在互联网领域取得突出成就，实现个人价值的同时为行业发展做出贡献。'
});
</script>

<template>
  <div class="resume-container">
    <!-- 左侧栏 -->
    <div class="resume-sidebar">
      <!-- 个人信息卡片 -->
      <div class="profile-card">
        <div class="avatar-container">
          <img :src="resumeData.avatarUrl" :alt="resumeData.name" class="avatar-image" />
        </div>
        <h1 class="name">{{ resumeData.name }}</h1>
        <p class="title">{{ resumeData.title }}</p>
        <div class="contact-info">
          <div class="contact-item">
            <Mail :size="14" class="icon" />
            <span>{{ resumeData.contact.email }}</span>
          </div>
          <div class="contact-item">
            <Phone :size="14" class="icon" />
            <span>{{ resumeData.contact.phone }}</span>
          </div>
        </div>
      </div>

      <!-- 教育背景 -->
      <div class="sidebar-section">
        <h2 class="section-title">
          <GraduationCap :size="16" class="icon" />
          教育背景
        </h2>
        <div class="education-content">
          <p class="school">{{ resumeData.education.school }}</p>
          <p class="degree">{{ resumeData.education.degree }}</p>
          <p class="graduation">{{ resumeData.education.graduationDate }}</p>
        </div>
      </div>

      <!-- 专业技能 -->
      <div class="sidebar-section">
        <h2 class="section-title">
          <Code :size="16" class="icon" />
          专业技能
        </h2>
        <div class="skills-content">
          <div v-for="(skillGroup, index) in resumeData.skills" :key="index" class="skill-group">
            <p class="skill-category">{{ skillGroup.category }}</p>
            <p class="skill-items">{{ skillGroup.items.join(' · ') }}</p>
          </div>
        </div>
      </div>

      <!-- 荣誉奖项 -->
      <div class="sidebar-section">
        <h2 class="section-title">
          <Award :size="16" class="icon" />
          荣誉奖项
        </h2>
        <ul class="achievements-list">
          <li v-for="(achievement, index) in resumeData.achievements" :key="index">
            {{ achievement }}
          </li>
        </ul>
      </div>
    </div>

    <!-- 右侧内容 -->
    <div class="resume-main">
      <!-- 职业目标 -->
      <div class="main-section">
        <h2 class="section-title">
          <Target :size="16" class="icon" />
          职业目标
        </h2>
        <p class="objective-text">{{ resumeData.careerObjective }}</p>
      </div>

      <!-- 项目经验 -->
      <div class="main-section">
        <h2 class="section-title">
          <Briefcase :size="16" class="icon" />
          项目经验
        </h2>
        <div class="projects-list">
          <div v-for="(project, index) in resumeData.projects" :key="index" class="project-item">
            <h3 class="project-title">{{ project.name }}</h3>
            <ul class="project-details">
              <li v-for="(item, idx) in project.description" :key="idx">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 工作经验 -->
      <div class="main-section">
        <h2 class="section-title">
          <Briefcase :size="16" class="icon" />
          工作经验
        </h2>
        <div class="experience-list">
          <div v-for="(job, index) in resumeData.experience" :key="index" class="experience-item">
            <div class="job-header">
              <h3 class="job-title">{{ job.title }}</h3>
              <span class="company-name">{{ job.company }}</span>
            </div>
            <p class="job-period">{{ job.period }}</p>
            <ul class="job-responsibilities">
              <li v-for="(resp, idx) in job.responsibilities" :key="idx">{{ resp }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 个人特质 -->
      <div class="main-section">
        <h2 class="section-title">
          <Star :size="16" class="icon" />
          个人特质
        </h2>
        <ul class="qualities-list">
          <li v-for="(quality, index) in resumeData.personalQualities" :key="index">
            {{ quality }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.resume-container {
  width: 210mm;
  min-height: 297mm;
  margin: 0 auto;
  display: flex;
  background: #ffffff;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.resume-sidebar {
  width: 280px;
  background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.resume-main {
  flex: 1;
  padding: 2rem;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 个人信息卡片样式 */
.profile-card {
  background: linear-gradient(135deg, #059669 0%, #0284c7 100%);
  padding: 1.5rem;
  border-radius: 1rem;
  color: white;
  text-align: center;
}

.avatar-container {
  width: 120px;
  height: 120px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.name {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.title {
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

/* 通用部分样式 */
.sidebar-section, .main-section {
  background: rgba(255, 255, 255, 0.9);
  padding: 1.25rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #047857;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.icon {
  color: #059669;
}

/* 教育背景样式 */
.education-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.school {
  font-weight: 600;
  color: #1f2937;
}

.degree, .graduation {
  color: #4b5563;
  font-size: 0.875rem;
}

/* 专业技能样式 */
.skill-group {
  margin-bottom: 0.75rem;
}

.skill-category {
  font-weight: 600;
  color: #047857;
  margin-bottom: 0.25rem;
}

.skill-items {
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* 列表样式 */
.achievements-list, .qualities-list, .project-details, .job-responsibilities {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.achievements-list li, .qualities-list li, .project-details li, .job-responsibilities li {
  position: relative;
  padding-left: 1.25rem;
  margin-bottom: 0.5rem;
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
}

.achievements-list li::before, .qualities-list li::before, .project-details li::before, .job-responsibilities li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #059669;
}

/* 项目经验样式 */
.project-item {
  margin-bottom: 1.25rem;
}

.project-title {
  font-weight: 600;
  color: #047857;
  margin-bottom: 0.5rem;
}

/* 工作经验样式 */
.experience-item {
  margin-bottom: 1.25rem;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}

.job-title {
  font-weight: 600;
  color: #047857;
}

.company-name {
  color: #6b7280;
  font-size: 0.875rem;
}

.job-period {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

/* 响应式设计 */
@media print {
  .resume-container {
    box-shadow: none;
  }
}

@media (max-width: 768px) {
  .resume-container {
    flex-direction: column;
    width: 100%;
  }

  .resume-sidebar {
    width: 100%;
  }
}
</style>
