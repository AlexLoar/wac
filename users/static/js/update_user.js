Vue.component('update-user', {
    data () {
        return {
            user: {},
            selectedFile: null
        }
    },
    created() {
            authToken = JSON.parse(localStorage.getItem('authKey'))
            axios.defaults.headers.common['Authorization'] = 'Token ' + authToken
            this.getUser();
        },
    methods: {
        getUser: function() {
                user = JSON.parse(localStorage.getItem('user'))

                axios.get('/api/v1/users/' + user)
                    .then(response => {
                        this.user = response.data;
                    })
                    .catch(error => {
                        M.toast({html: 'Ooops! Something went wrong...'}, 3000);
                    })
            },
        bodyToSend: function () {
            body = {
                name: this.$refs['user_name'].value,
                first_name: this.$refs['user_first_name'].value,
                last_name: this.$refs['user_last_name'].value,
                email: this.$refs['user_email'].value,
            };
            formData = new FormData()
            formData.append('avatar', this.selectedFile, this.selectedFile.name)
            for (var key in body) {
                formData.append(key, body[key])
            }
            return formData
        },
        updateUser: function () {
            authToken = JSON.parse(localStorage.getItem('authKey'))
            axios.defaults.headers.common['Authorization'] = 'Token ' + authToken
            url = '/api/v1/users/' + this.user.id;
            axios.put(url, this.bodyToSend(),
                {uploadProgress: uploadEvent => {
                                console.log('Upload progress: ' + Math.round(uploadEvent.loaded / uploadEvent.total * 100) + '%')
                            }})
                .then(response => {
                    this.getUser()
                    console.log(response)
            })
            .catch(error => {
                console.log(error);
            })
        },
        onFileSelected(event) {
            this.selectedFile = event.target.files[0]
        }
    },
    template: `
        <div id="update-user" class="">
        <h3>User</h3>
        
        <div id="form-user">
            <form v-on:submit.prevent>
                <div class="form-group">
                    <label for="user_id">ID</label>
                    <input type="text" class="form-control" disabled v-model="user.id" id="user_id">
                </div>
        
                <div class="form-group">
                    <label for="user_name">Name</label>
                    <input type="text" class="form-control" v-model="user.name" ref="user_name">
                </div>
        
                <div class="form-group">
                    <label for="user_first_name">First name</label>
                    <input type="text" class="form-control" v-model="user.first_name" ref="user_first_name">
                </div>
        
                <div class="form-group">
                    <label for="user_last_name">Last name</label>
                    <input type="text" class="form-control" v-model="user.last_name" ref="user_last_name">
                </div>
        
                <div class="form-group">
                    <label for="user_email">Email</label>
                    <input type="email" class="form-control" v-model="user.email" ref="user_email">
                </div>
        
                <div class="input-group">
                    <img v-if="user.avatar" :src="[[ user.avatar ]]" id="user_avatar" class="responsive-img" width="60" height="60" alt="Avatar">
                    <input type="file" style="display: none" @change="onFileSelected" ref="imageInput"><br>
                    <button @click="$refs.imageInput.click()" class="waves-effect waves-light btn-small">Upload<i class="material-icons">file_upload</i></button>
                </div>
                <hr>
                
                <div class="form-group">
                    <button  v-on:click="updateUser" class="waves-effect waves-light red btn-large">Update</button>
                </div>
            </form>
        </div>
    </div>
    `
});

Vue.config.devtools = true;
new Vue({
  el: '#app',
  delimiters: ['[[', ']]']
});
