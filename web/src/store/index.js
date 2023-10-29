import { createStore } from 'vuex'
import menu from './menu'
import user from './user'

export default createStore({
  modules: {
    menu, user
  }
})
