<template>
<v-container class="pa-2 edit-form" >
  <div v-if="this.currentItem">
    <h1>Item details</h1>

    <v-form ref="form" lazy-validation>
      <v-text-field
        v-model="currentItem.id"
        label="ID"
        readonly
        shaped
        filled
      ></v-text-field>

      <v-text-field
        v-model="currentItem.name"
        :rules="[(v) => !!v || 'Name is required']"
        label="Name"
        required
        outlined
      ></v-text-field>

      <v-radio-group label="Type" v-model="currentItem.type">
        <v-radio name="type" label="Tool" value="tool"></v-radio>
        <v-radio name="type" label="Command" value="command"></v-radio>                
      </v-radio-group>

      <v-textarea
          label="Description"
          :rules="[(v) => !!v || 'Description is required']"
          required
          hint="Description, keywords"
          v-model="currentItem.description"
          outlined
        ></v-textarea>

        <v-textarea
          label="Usage"
          :rules="[(v) => !!v || 'Usage is required']"
          required
          hint="Usage, commands"
          v-model="currentItem.usage"
          outlined
        ></v-textarea>

        <v-text-field
        v-model="currentItem.source"
        label="Source/site"
        :rules="[(v) => !!v || 'Source is required']"
        required
        outlined
      ></v-text-field>

      <v-text-field
        v-model="currentItem.cve"
        label="CVE"
        hint="Format: cve-year-serialnumber (cve-2022-1234) or leave empty"
        outlined
      ></v-text-field>

      <v-row>
        <v-col>
          <p>Attack OS(es)</p>
        </v-col>
      </v-row>
      <hr>
      <v-row>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.attackos"
              label="linux"
              value="linux"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.attackos"
              label="windows"
              value="windows"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.attackos"
              label="mac"
              value="mac"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.attackos"
              label="other"
              value="other"
              hide-details
            ></v-checkbox>
          </v-col>
      </v-row>

      <v-row>
        <v-col>
          <p>Phases</p>
        </v-col>
      </v-row>
      <hr>

        <v-row>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.phase"
              label="recon"
              value="recon"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.phase"
              label="scanning"
              value="scanning"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.phase"
              label="initial foothold"
              value="initial foothold"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.phase"
              label="privesc"
              value="privesc"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.phase"
              label="maintain access"
              value="maintain access"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.phase"
              label="covering"
              value="covering"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.phase"
              label="general"
              value="general"
              hide-details
            ></v-checkbox>
          </v-col>
        </v-row>

      
        <div class="text-center mt-3 pa-3">
          <v-btn color="success"  @click="updateItem" >
            Update
          </v-btn>

          <v-btn v-if="this.role < 1" color="error"  @click="deleteItem" >
            Delete
          </v-btn>
        </div>

    </v-form>
  </div>

  <div v-else>
    <p>Please select an item...</p>
  </div>
</v-container>
</template>

<script>
import axios from 'axios';
import { mapMutations } from "vuex";
import jwt_decode from "jwt-decode";
import store from '../store';

export default {
  name: "tutorial",
  data: function() {
    return {
      data: null,
      currentItem: null,
      role: null
    };
  },
  methods: {
    ...mapMutations(["setToken"]),
    getItem(id) {
      const path = 'http://127.0.0.1:5001/api/item/'+ id;
      axios.get(path, )
        .then((res) => {
          this.data = res.data;
          this.currentItem = this.data.item
        })
        .catch((error) => {
          console.error(error);
        });
    },
    updateItem() {
      const pathUpdate = 'http://127.0.0.1:5001/api/item/'+ this.currentItem.id +'/update'
      const headers = {
        'Authorization': 'Bearer '+ this.$store.getters.token
      }
      axios.post(pathUpdate, this.currentItem, { headers: headers },
       ).then(response => {
          if (response.data['token'])
            this.setToken(response.data['token'])
        }).catch(err =>{
          if(err.response.status === 666){
            console.log(err.response.data)
            this.$alert(err.response.data, "Verification failed")
            this.$router.push('/login')
          }else if(err.response.status === 403){
            this.$alert(err.response.data, "Verification failed")
          }
        });    
    },
    deleteItem() {
      const headers = {
        'Authorization': 'Bearer '+ this.$store.getters.token
      }
      const path = 'http://127.0.0.1:5001/api/item/'+ this.currentItem.id +'/delete'
      axios.delete(path, {headers: headers} , this.currentItem
      ).then(response => {
        console.log(response)
        if (response.data['token'])
            this.setToken(response.data['token'])
        this.$alert(response.data['message'], "Item deleted")
        this.$router.push("/items")
      }).catch(err =>{
          if(err.response.data.includes("invalid"))
            this.$alert(err.response.data, "Authentication failure")
            this.$router.push('/login')
      });
    },
    // sendValidation(){
    //   const pathValidate = 'http://127.0.0.1:5001/api/validate'
    //   const headers = {
    //     'Authorization': 'Bearer '+ this.$store.getters.token
    //   }
    //   axios.post(pathValidate, this.user, { headers: headers }
    //   ).then(response => {
    //     this.res = response
    //     while (this.res === null){
    //       console.log(this.res)
    //     }
    //   }).catch(err =>{
    //     console.log(err);
    //   });
    // },
    // validate(){
    //   if (this.res.status == 200){
    //       //this.setValidation(true)
    //       if (this.res.data["token"]){
    //         this.setToken(response.data["token"])
    //         console.log("VALIDATE NEW", this.$store.getters.token)
    //         return true
    //       }
    //       return true
    //   }else{
    //     return false
    //   }
    // }
  },
  mounted() {
    this.getItem(this.$route.params.id);
    this.role = jwt_decode(this.$store.getters.token)['role']
  }
};
</script>

<style>
.edit-form {
  max-width: 50%;
  margin: auto;
}
</style>
