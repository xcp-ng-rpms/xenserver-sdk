def build() {

  node("linux") {

    stage('Download dependencies') {
      deleteDir()
      unstash name: "${env.JOB_NAME}.${env.BUILD_NUMBER}.post_setup"

      def server = Artifactory.server('repo')
      String downloadSpec = readFile("${env.WORKSPACE}/deps-map.json").trim()
      server.download(downloadSpec)
    }

    stage('Build Linux') {
      sh "${dockerRun} '. build-before.sh' "
      stash include: '*', name: "${env.JOB_NAME}.${env.BUILD_NUMBER}.post_linux"
    }
  }

  node("windows") {

    stage('Build Windows') {
      deleteDir()

      unstash name: "${env.JOB_NAME}.${env.BUILD_NUMBER}.post_linux"

      bat "build-win.bat ${env.SNK_LOCATION}"

      stash include: '*', name: "${env.JOB_NAME}.${env.BUILD_NUMBER}.post_win"
    }
  }

  node("linux") {
    stage('Package') {
      deleteDir()
      unstash name: "${env.JOB_NAME}.${env.BUILD_NUMBER}.post_win"
      sh "${dockerRun} '. build-after.sh' "
    }

    stage('Upload') {
      def server = Artifactory.server('repo')
      def buildInfo = Artifactory.newBuildInfo()
      buildInfo.env.filter.addInclude("*")
      buildInfo.env.collect()

      // IMPORTANT: do not forget the slash at the end of the target path!
      GString uploadSpec = """ {
      "files": [{
          "pattern": "*.zip",
          "flat": "true",
          "target": "${params.UPLOAD_LOCATION}/",
          "props": "vcs.revision=;build.number=${env.BUILD_NUMBER};build.name=${env.JOB_NAME};vcs.branch=${env.BRANCH_NAME};vcs.url=${env.GIT_URL}"
        }]
      }
      """

      def buildInfo_upload = server.upload(uploadSpec)
      buildInfo.append buildInfo_upload
      server.publishBuildInfo buildInfo
    }
  }

}

return this
