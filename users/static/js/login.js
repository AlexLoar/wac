Vue.component('user-login', {
    data () {
        return {
            username: null,
            password: null,
            auth: {}
        }
    },
    methods: {
        login: function() {
            body_request = {username: this.username, password: this.password}

            axios.post('/api/v1/login', body_request)
                .then(response => {
                    this.auth = response.data
                    localStorage.clear()
                    localStorage.setItem('authKey', JSON.stringify(this.auth.token))
                    localStorage.setItem('user', JSON.stringify(this.auth.user))
                    this.redirectUser()
                })
                .catch(error => {
                    M.toast({html: 'Bad username or password'}, 5000)
                    console.log(error)
                })
        },
        redirectUser() {
            let currentDomain = window.location.href.split('/')[0];
            let formListLocation = currentDomain + '/users';

            window.location.replace(formListLocation)
        }
    },
    template: `
  <div>
    <h1>Log In</h1>
      <div class="row center">
      <form v-on:submit.prevent="onSubmit">
        <div class="input-field col s6">
          <input id="username" name="username" type="text" v-model="username" class="validate">
          <label class="active" for="username">Username</label>
        </div>
        <div class="input-field col s6">
          <input id="password" name="password" type="password" v-model="password" class="validate">
          <label class="active" for="password">Password</label>
        </div>
        <div class="input-field col s12">
          <button class="btn waves-effect waves-light"
                  v-on:click="login"
                  name="action">
                  Login
          </button>
        </div>
        </form>
      </div>
  </div>
`
});

Vue.config.devtools = true;
new Vue({
  el: '#app'
});
