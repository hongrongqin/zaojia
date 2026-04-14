import { defineStore } from 'pinia';

// defineStore 的第一个参数是 store 的唯一 ID。
// 这个 ID 是 Pinia 连接 DevTools 的关键，必须是唯一的。
export const useMainStore = defineStore('main', {
    /**
     * State
     * 类似于组件的 data，但必须是一个函数，返回初始状态。
     * 这样做可以确保在服务端渲染(SSR)时避免状态交叉污染。
     */
    state: () => ({
        userInfo: {
            userId: '',
            userName: '',
            userRole: '',
            userToken: ''
        },
        isLogin: false,
        dynamicData: {} // 用于存储动态数据
    }),

    /**
     * Getters
     * 类似于组件的 computed 属性。它们是响应式的，并且会被缓存。
     */
    getters: {
        /**
         * Pinia 中实现带参数的 getter，需要返回一个函数。
         * 外层函数接收 state，内层函数接收你的参数。
         * @param {object} state - 当前 store 的 state
         */
        getDynamicData: (state) => {
            return (key) => state.dynamicData[key];
        },

        // 你也可以添加其他普通的 getters
        isUserLoggedIn: (state) => state.isLogin && !!state.userInfo.userId,
    },

    /**
     * Actions
     * 类似于组件的 methods。它们可以用来修改 state，
     * 并且可以是异步的 (async/await)。
     * Pinia 中没有 mutations，所有的状态变更都在 actions 中完成。
     */
    actions: {
        /**
         * 动态添加数据。
         * 在 actions 中，你可以通过 `this` 直接访问和修改 state。
         * 这比 Vuex 的 commit('mutation', payload) 更直观。
         * @param {string} key
         * @param {*} value
         */
        addDynamicData(key, value) {
            this.dynamicData[key] = value;
        },

        /**
         * 删除动态数据。
         * @param {string} key
         */
        removeDynamicData(key) {
            delete this.dynamicData[key];
        },

        // 示例：一个登录的 action
        login(userData) {
            this.userInfo = { ...this.userInfo, ...userData };
            this.isLogin = true;
            // 可以直接在这里进行 API 调用
            // const response = await api.login(userData);
            // this.userInfo.userToken = response.data.token;
        },

        logout() {
            // 使用 $reset() 方法可以方便地将 state 重置为初始状态
            this.$reset();
        }
    }
});
