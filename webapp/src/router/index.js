import Vue from 'vue'
import Router from 'vue-router'
import LoginPage from '@/components/pages/LoginPage'
import AnalyzePage from '@/components/pages/AnalyzePage'
import ProblemsPage from '@/components/pages/ProblemsPage'
import ProfilePage from '@/components/pages/ProfilePage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'Login',
      label: 'LOGIN',
      hidden: true,
      component: LoginPage
    },
    {
      path: '/problems',
      name: 'Problems',
      label: 'PROBLEMS',
      component: ProblemsPage
    },
    {
      path: '/analyze',
      name: 'Analyze',
      label: 'ANALYZE',
      component: AnalyzePage
    },
    {
      path: '/profile',
      name: 'Profile',
      label: 'PROFILE',
      component: ProfilePage
    },
    {
      path: '',
      redirect: 'login'
    }
  ]
})
