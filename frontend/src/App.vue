<template>
  <v-app>
    <v-navigation-drawer v-if="this.$store.getters.token"
      v-model="drawer"
      app
      clipped
    >
      <v-list dense>
        <v-list-item
          v-for="item in items"
          :key="item.text"
          :to="item.to"
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              {{ item.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
      color="lime darken-2"
      dense
    >
      <v-app-bar-nav-icon v-if="this.$store.getters.token" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-icon class="mx-4">mdi-incognito</v-icon>
      <v-toolbar-title class="mr-12 align-center">
        <span class="title">LeutMesiene - Hacker Cheatsheet</span>
      </v-toolbar-title>
      <v-row justify="end">
        <v-btn v-if="!this.$store.getters.token" color="teal darken-2" :to="'/login'">Login</v-btn>
        <v-btn v-else color="red darken-2" @click="logout" :to="'/login'">Logout</v-btn>
      </v-row>
    </v-app-bar>

    <v-content>
      <v-container fluid fill-height>
        <v-layout fluid>
          <router-view></router-view>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapMutations } from "vuex";
export default {
  name: 'App',
   data: () => ({
      drawer: null,
      items: [
        { icon: 'mdi-database-lock', text: 'List of items', to: '/items' },
        { icon: 'mdi-plus-circle-outline', text: 'Add new item', to: '/add-item' },
        { icon: 'mdi-account', text: 'Account' , to: '/login'}
      ]
    }),
  methods: {
    ...mapMutations(["setUser", "setToken"]),
    logout(){
      this.setUser(null)
      this.setToken(null)
    }
  },
  created () {
      this.$vuetify.theme.dark = true
  }
}
</script>

<style>
</style>
