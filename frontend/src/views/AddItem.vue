<template>
<v-container class="pa-2 edit-form" >
    <h1>New item</h1>

    <v-form ref="form" lazy-validation>
      <!-- <v-text-field
        v-model="currentItem.id"
        label="ID"
        readonly
        shaped
        filled
      ></v-text-field> -->

      <v-text-field
        v-model="name"
        :rules="[(v) => !!v || 'Name is required']"
        label="Name"
        required
        outlined
      ></v-text-field>

      <v-radio-group label="Type" v-model="type">
        <v-radio name="type" label="Tool" value="tool"></v-radio>
        <v-radio name="type" label="Command" value="command"></v-radio>                
      </v-radio-group>

      <v-textarea
          label="Description"
          :rules="[(v) => !!v || 'Description is required']"
          required
          hint="Description, keywords"
          v-model="description"
          outlined
        ></v-textarea>

        <v-textarea
          label="Usage"
          :rules="[(v) => !!v || 'Usage is required']"
          required
          hint="Usage, commands"
          v-model="usage"
          outlined
        ></v-textarea>

        <v-text-field
        v-model="source"
        label="Source/site"
        :rules="[(v) => !!v || 'Source is required']"
        required
        outlined
      ></v-text-field>

      <v-text-field
        v-model="cve"
        hint="Format: cve-year-serialnumber (cve-2022-1234) or leave empty"
        label="CVE"
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
              v-model="attackos"
              label="linux"
              value="linux"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="attackos"
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
              v-model="attackos"
              label="mac"
              value="mac"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="attackos"
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
              v-model="phase"
              label="recon"
              value="recon"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="phase"
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
              v-model="phase"
              label="initial foothold"
              value="initial foothold"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="phase"
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
              v-model="phase"
              label="maintain access"
              value="maintain access"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="phase"
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
              v-model="phase"
              label="general"
              value="general"
              hide-details
            ></v-checkbox>
          </v-col>
        </v-row>

      
        <div class="text-center mt-3 pa-3">
          <v-btn color="success"  @click="AddItem" >
            Add
          </v-btn>
        </div>
    </v-form>
</v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: "tutorial",
  data: function() {
    return {
      data: null,
      currentItem: null,
      name: "",
      type: "",
      description: "",
      usage: "",
      source: "",
      cve: "",
      attackos: [],
      phase: "",
      

    };
  },
  methods: {
    AddItem() {
      this.currentItem = {name: this.name, 
                          type: this.type,
                          description: this.description,
                          usage: this.usage,
                          source: this.source,
                          cve: this.cve,
                          attackos: this.attackos,
                          phase: this.phase}
      console.log(this.currentItem)
      
      const path = 'http://127.0.0.1:5001/api/item/add'
      axios.post(path, this.currentItem
      ).then(response => {
        console.log(response);
        this.$router.push("/item/"+ response.data.item.id)
      }).catch(err =>{
        console.log("failed")
        this.$alert("You made a mistake with filling everything in", "Syntax error")
      });
    },
    
  },
  mounted() {
      
  }
};
</script>

<style>
.edit-form {
  max-width: 50%;
  margin: auto;
}
</style>
