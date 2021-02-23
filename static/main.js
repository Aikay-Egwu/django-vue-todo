const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',  
  }
});

var app = new Vue({
  el: '#app',
  data: {
    task: {title: ''},
    csrf: null,
    tasks: [],
    completed: {
      color: 'red',
    }
  },
  async created() {
    await this.allTasks()
  },
  computed:{
    
  },
  methods: {
    async networkRequest(url, method, data) {

      if (method !== 'get') {
        //heads.set('X-CSRFToken', await this.getCsrfToken()) 
        instance.defaults.headers.common['X-CSRFToken'] = await this.getCsrfToken()
      }
      return await instance({
        url: url,
        method: method,
        data: data
      })
    },
    async getCsrfToken(){
      if (this.csrf === null){
        const response = await this.networkRequest('tasks/csrf', 'get', '')

        //var response = await instance.get('tasks/csrf')
        this.csrf = response.data.csrf_token
      }
      return this.csrf 
    },
    async add() {
      const response = await this.networkRequest('tasks/create', 'post', JSON.stringify(this.task))

      /* var response = await instance.post('tasks/create',
        JSON.stringify(this.task),
        {
          headers: {
            'X-CSRFToken': await this.getCsrfToken()
          }
        }
      ) */
      this.allTasks()
      this.task = ''
    },
    async allTasks() {
      //var response = await instance.get('tasks')
      const response = await this.networkRequest('tasks', 'get', '')
      this.tasks = response.data
    },
    async markCompleted(task) {
      const response = await this.networkRequest('tasks/update', 'put', JSON.stringify(task))
      console.log(response)
    },
    async deleteTask(task) {
      const response = await this.networkRequest('tasks/delete', 'delete', JSON.stringify(task))
      console.log(response)
      //await instance.delete('', JSON.stringify(task))
      await this.allTasks()
    }
  }
})