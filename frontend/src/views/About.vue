<template>
  
  <v-card class="mx-auto" color="grey lighten-4" max-width="600">
    <v-card-title>
      <h1 :style="{color: ' #f67e7e'}"> User: {{ this.user }} </h1>
      <v-icon :color="checking ? 'red lighten-2' : 'indigo'" class="mr-5" size="64" @click="takePulse">
        mdi-heart-pulse
      </v-icon>
      <v-layout column align-start>
        <div class="caption grey--text text-uppercase">
          Heart rate
        </div>
        <div :style="{color: ' #f67e7e'}">
          <span class="display-2 font-weight-black" v-text="avg || '—'"></span>
          <strong v-if="avg">BPM</strong>
        </div>
      </v-layout>
      <v-spacer></v-spacer>
      <v-btn icon class="align-self-start" size="28">
        <v-icon>mdi-arrow-right-thick</v-icon>
      </v-btn>
    </v-card-title>

    <v-sheet color="transparent">
      <v-sparkline :smooth="16" :gradient="['#f72047', '#ffd200', '#1feaea']" :line-width="3" :key="String(avg)" :value="heartbeats" auto-draw
        stroke-linecap="round"
      ></v-sparkline>
    </v-sheet>
    <p :style="{color: ' #000000'}">TEST purposes: {{ this.token }} </p>
  </v-card>
</template>


<script>
import store from '../store'

  const exhale = ms =>
    new Promise(resolve => setTimeout(resolve, ms))
  export default {
    data: () => ({
      checking: false,
      heartbeats: [],
      user: null,
      token: null
    }),
    computed: {
      avg () {
        const sum = this.heartbeats.reduce((acc, cur) => acc + cur, 0)
        const length = this.heartbeats.length
        if (!sum && !length) return 0
        return Math.ceil(sum / length)
      }
    },
    created () {
      this.takePulse(false),
      this.user = this.$store.getters.user,
      this.token = this.$store.getters.token
    },
    methods: {
      heartbeat () {
        return Math.ceil(Math.random() * (120 - 80) + 80)
      },
      async takePulse (inhale = true) {
        this.checking = true
        inhale && await exhale(1000)
        this.heartbeats = Array.from({ length: 20 }, this.heartbeat)
        this.checking = false
      }
    }
  }
</script>