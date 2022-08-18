<template>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md4>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="lime darken-2"">
                        <v-toolbar-title>Login form</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                        <v-form>
                           <v-text-field
                              prepend-icon="mdi-account"
                              name="login"
                              label="Login"
                              type="text"
                              v-model="username"
                           ></v-text-field>
                           <v-text-field
                              id="password"
                              prepend-icon="mdi-lock"
                              name="password"
                              label="Password"
                              type="password"
                              v-model="password"
                           ></v-text-field>
                        </v-form>
                     </v-card-text>
                     <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="teal darken-2" @click="login">Login</v-btn>
                     </v-card-actions>
                  </v-card>
               </v-flex>
            </v-layout>
         </v-container>
</template>

<script>
import axios from 'axios';
import { mapMutations } from "vuex";
import { mapGetters } from "vuex";

export default {
  data: function() {
    return {
      data: null,
      username: "",
      password: "",
      login_user: null,
    };
  },
  methods: {
    ...mapMutations(["setUser", "setToken"]),
    login() {
      this.login_user = {username: this.username,
                  password: this.password}
      const path = 'http://127.0.0.1:5001/api/login'
      axios.post(path, this.login_user
      ).then(response => {
         //Set user and token in vuex store, https://vuex.vuejs.org/guide/getters.html
         this.setUser(response.data["user"])
         this.setToken(response.data["token"])
         console.log(this.$store.getters.user, this.$store.getters.token)
      }).catch(err =>{
        console.log(err);
      });
    }
  }
};
</script>
