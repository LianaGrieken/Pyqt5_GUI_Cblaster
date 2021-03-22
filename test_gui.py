from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtWidgets import QButtonGroup, QFileDialog, QLineEdit


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        # Load the .ui file
        uic.loadUi('main_window.ui', self)

        # Hide options that are not needed when first initializing window
        self.hide_options()

        # Button groups
        self.make_bgroup_search()
        self.make_bgroup_binary_key()
        self.make_bgroup_binary_hit()

        # Event: Change tab index when clicked
        self.tabs_Cblaster.currentChanged.connect(self.change_tabindex)
        # Event: Exit program
        self.pb_exit.clicked.connect(self.exit_cblaster)
        # Event: Save options
        self.pb_save.clicked.connect(self.save_options)
        # Event: Load options
        self.pb_load.clicked.connect(self.load_options)
        # Event: Start button, get input options
        self.pb_start.clicked.connect(self.start_cblaster)
        # Event: Open file dialog for all browse and save buttons
        list_bt_browse_file = [self.pb_sDiaBrowse, self.pb_inBrowse,
                               self.pb_sFasBrowse,self.pb_sPfamBrowse,
                               self.pb_flSave, self.pb_stSave,
                               self.pb_btSave, self.pb_fSave, self.pb_nBrowse,
                               self.pb_nSaveOut,self.pb_nSavePlot,
                               self.pb_mdbBrowse, self.pb_mdbSave,
                               self.pb_exBrowse, self.pb_exSave,
                               self.pb_ecBrowseSess, self.pb_pcBrowseSes]
        for bt in list_bt_browse_file:
            bt.clicked.connect(self.open_file_dialog)
        list_bt_browse_dir = [self.pb_ecBrowseOut, self.pb_pcBrowseOut]
        for bt in list_bt_browse_dir:
            bt.clicked.connect(self.open_dir_dialog)

        # Show
        self.show()

    def open_dir_dialog(self):
        dir = QFileDialog.getExistingDirectory()
        obj_name = self.sender().objectName()
        le_name = "le" + obj_name[2:]
        line_edit = self.findChild(QLineEdit, le_name)
        line_edit.setText(dir)

    def open_file_dialog(self):
        file = QFileDialog.getOpenFileName()
        obj_name = self.sender().objectName()
        le_name = "le" + obj_name[2:]
        line_edit = self.findChild(QLineEdit, le_name)
        line_edit.setText(file[0])

    def change_tabindex(self):
        self.tabs_Cblaster.currentIndex()

    def exit_cblaster(self):
        sys.exit()

    def start_cblaster(self):
        tab_lbl = self.tabs_Cblaster.tabText(self.tabs_Cblaster.currentIndex())
        print(tab_lbl)

    def save_options(self):
        file = open("Options_Saved.txt", "w")
        search_list = self.get_search_options()
        filter_list = self.get_filter_options()
        summary_list = self.get_summary_table_options()
        binary_list = self.get_binary_table_options()
        figure_list = self.get_figure_options()
        neigh_list = self.get_neighbourhood_options()
        makedb_list = self.get_makedb_options()
        extract_list = self.get_extract_options()
        exclust_list = self.get_extractClusters_options()
        plot_list = self.get_plotCluster_options()
        file.write("Search {} {} {} {} {}\n".format(str(search_list), str(filter_list),
                                                  str(summary_list), str(binary_list),
                                                  str(figure_list)))
        file.write("Neighbourhood {} \n".format(str(neigh_list)))
        file.write("Makedb {}\n".format(str(makedb_list)))
        file.write("Extract {} \n".format(str(extract_list)))
        file.write("Extract_Clusters {} \n".format(str(exclust_list)))
        file.write("Plot_Clusters {}".format(str(plot_list)))
        file.close()

    def load_options(self):
        tab_lbl = self.tabs_Cblaster.tabText(self.tabs_Cblaster.currentIndex())
        file = open("Options_Saved.txt", "r")
        line_list = file.read().split("\n")
        for item in line_list:
            tab_name = item.split(" ")[0]
            if tab_name.replace("_", " ") == tab_lbl:
                self.find_call_function("set_options_" + tab_name, item)
        file.close()

    def find_call_function(self, fun_name, options):
        func = getattr(self, fun_name)
        func(options)

    def set_options_Search(self, options):
        op_ls = options.split("(")
        #search mode #1
        op = op_ls[1].replace("'", "").replace(" ", "").strip(")").split(",")
        if op[0] == "Local":
            self.le_inBrowse.setText(op[1])
            self.le_sDiaBrowse.setText(op[2])
            self.le_sCPU.setText(op[3])
        elif op[0] == "Remote":
            self.le_inBrowse.setText(op[1])
            self.le_sDB.setText(op[2])
            self.le_sEntrz.setText(op[3])
            self.le_sRID.setText(op[4])
            self.le_sMaxHits.setText(op[5])
        elif op[0] == "HMMER":
            self.le_inHmm.setText(op[1])
            self.le_sDiaBrowse.setText(op[2])
            self.le_sFasBrowse.setText(op[3])
            self.le_sPfamBrowse.setText(op[4])
        elif op[0] == "Combilocal":
            self.le_inBrowse.setText(op[1])
            self.le_sDiaBrowse.setText(op[2])
            self.le_sCPU.setText(op[3])
            self.le_inHmm.setText(op[4])
            self.le_sFasBrowse.setText(op[5])
            self.le_sPfamBrowse.setText(op[6])
        elif op[0] == "Combiremote":
            self.le_inBrowse.setText(op[1])
            self.le_sDB.setText(op[2])
            self.le_sEntrz.setText(op[3])
            self.le_sRID.setText(op[4])
            self.le_sMaxHits.setText(op[5])
            self.le_inHmm.setText(op[6])
            self.le_sDiaBrowse.setText(op[7])
            self.le_sFasBrowse.setText(op[8])
            self.le_sPfamBrowse.setText(op[9])
        #Filtering #2
        op = op_ls[2].replace("'", "").replace(" ", "").strip(")").split(",")
        self.le_fMaxEval.setText(op[0])
        self.le_fMinId.setText(op[1])
        self.le_fQuCov.setText(op[2])
        self.ch_fRecom.setChecked(bool(op[3]))
        self.le_flSave.setText(op[4])
        #Summary table #3
        op = op_ls[3].replace("'", "").replace(" ", "").strip(")").split(",")
        self.ch_SumTab.setChecked(bool(op[0]))
        self.le_stDeli.setText(op[1])
        self.lb_stDecimal.setText(op[2])
        self.ch_stSort.setChecked(bool(op[3]))
        self.ch_stHide.setChecked(bool(op[4]))
        self.le_stSave.setText(op[5])
        #Binary table #4
        op = op_ls[4].replace("'", "").replace(" ", "").strip(")").split(",")
        self.ch_BinaryTab.setChecked(bool(op[0]))
        self.ch_btHide.setChecked(bool(op[1]))
        ##TODO: checking how to set buttongroup selection with text ##
        self.bt_groupKey.checkedButton().text()
        self.bt_groupHit.checkedButton().text()
        ##END
        self.lb_btDeci.setText(op[4])
        self.le_btSave.text(op[5])
        #Figure #5
        op = op_ls[5].replace("'", "").replace(" ", "").strip(")").split(",")
        self.ch_Figure.setChecked(bool(op[0]))
        self.le_fSave.setText(op[1])

    def set_options_Neighbourhood(self, options):
        op_ls = options.split("(")
        op = op_ls[1].replace("'", "").replace(" ", "").strip(")").split(",")
        self.le_nBrowse.setText(op[0])
        self.le_nSaveOut.setText(op[1])
        self.le_nDeli.setText(op[2])
        self.le_nSavePlot.setText(op[3])
        self.le_max.setText(op[4])
        self.le_samNr.setText(op[5])
        ##TODO: checking how to set buttongroup selection with text ##
        # self.bt_groupSampSpace.checkedButton().text()
        ##END
        self.lbl_nSliderVal.setText(op[7])
        self.ch_nHide.setChecked(bool(op[8]))

    def set_options_Makedb(self, options):
        op_ls = options.split("(")
        op = op_ls[1].replace("'", "").replace(" ", "").strip(")").split(",")
        self.le_mdbBrowse.setText(op[0])
        self.le_mdbSave.setText(op[1])
        self.le_mNrCPU.setText(op[2])
        self.le_mBatch.setText(op[3])
        self.ch_mOver.setChecked(bool(op[4]))

    def set_options_Extract(self, options):
        op_ls = options.split("(")
        op = op_ls[1].replace("'", "").replace(" ", "").strip(")").split(",")
        self.le_exBrowse.setText(op[0])
        self.le_exSave.setText(op[1])
        self.le_eQseq.setText(op[2])
        self.le_eOrg.setText(op[3])
        self.le_eSca.setText(op[4])
        self.le_eDel.setText(op[5])
        self.ch_Down.setChecked(bool(op[6]))
        self.ch_name.setChecked(bool(op[7]))

    def set_options_Extract_Clusters(self, options):
        op_ls = options.split("(")
        op = op_ls[1].replace("'", "").replace(" ", "").strip(")").split(",")
        self.le_ecBrowseSess.setText(op[0])
        self.le_ecBrowseOut.setText(op[1])
        self.le_ecPre.setText(op[2])
        ##TODO: checking how to set buttongroup selection with text ##
        #self.bt_groupOutput.checkedButton().text()
        ##END
        self.le_ecClus.setText(op[4])
        self.le_ecScThr.setText(op[5])
        self.le_ecOrg.setText(op[6])
        self.le_ecScaf.setText(op[7])
        self.lb_ecMaxClu.setText(op[8])

    def set_options_Plot_Clusters(self, options):
        op_ls = options.split("(")
        op = op_ls[1].replace("'", "").replace(" ", "").strip(")").split(",")
        self.le_pcBrowseSes.setText(op[0])
        self.le_pcBrowseOut.setText(op[1])
        self.le_pcClu.setText(op[2])
        self.le_pcScThr.setText(op[3])
        self.le_pcOrg.setText(op[4])
        self.lepcScaf.setText(op[5])
        self.lb_pcMaxClu.setText(op[6])

    def get_extract_options(self):
        session = self.le_exBrowse.text()
        output = self.le_exSave.text()
        qSeq = self.le_eQseq.text()
        org = self.le_eOrg.text()
        scaff = self.le_eSca.text()
        delim = self.le_eDel.text()
        down = self.ch_Down.isChecked()
        name_only = self.ch_name.isChecked()
        return session, output, qSeq, org, scaff, delim, down, name_only

    def get_makedb_options(self):
        gen = self.le_mdbBrowse.text()
        db_name = self.le_mdbSave.text()
        cpu_nr = self.le_mNrCPU.text()
        batch = self.le_mBatch.text()
        overwrite = self.ch_mOver.isChecked()
        return gen, db_name, cpu_nr, batch, overwrite

    def get_neighbourhood_options(self):
        session = self.le_nBrowse.text()
        output = self.le_nSaveOut.text()
        delimiter = self.le_nDeli.text()
        plot = self.le_nSavePlot.text()
        intMax = self.le_max.text()
        nrSam = self.le_samNr.text()
        self.bt_groupSampSpace = QButtonGroup()
        self.bt_groupSampSpace.addButton(self.rb_linear)
        self.bt_groupSampSpace.addButton(self.rb_log)
        samplSpace = self.bt_groupSampSpace.checkedButton().text()
        decimal = self.lbl_nSliderVal.text()
        hide_headers = self.ch_nHide.isChecked()
        return session, output, delimiter, plot, intMax, nrSam, samplSpace, \
               decimal, hide_headers

    def get_extractClusters_options(self):
        session = self.le_ecBrowseSess.text()
        output = self.le_ecBrowseOut.text()
        prefix = self.le_ecPre.text()
        self.bt_groupOutput = QButtonGroup()
        self.bt_groupOutput.addButton(self.rb_bigscape)
        self.bt_groupOutput.addButton(self.rb_genbank)
        outFormat = self.bt_groupOutput.checkedButton().text()
        clusters = self.le_ecClus.text()
        score = self.le_ecScThr.text()
        orgs = self.le_ecOrg.text()
        scaff = self.le_ecScaf.text()
        maxClust = self.lb_ecMaxClu.text()
        return session, output, prefix, outFormat, clusters, score, orgs, \
               scaff, maxClust

    def get_plotCluster_options(self):
        session = self.le_pcBrowseSes.text()
        output = self.le_pcBrowseOut.text()
        clusters = self.le_pcClu.text()
        score = self.le_pcScThr.text()
        orgs = self.le_pcOrg.text()
        scaff = self.lepcScaf.text()
        maxClust = self.lb_pcMaxClu.text()
        return session, output, clusters, score, orgs, scaff, maxClust

    def make_bgroup_search(self):
        self.bt_groupSearch = QButtonGroup()
        self.bt_groupSearch.addButton(self.rb_local)
        self.bt_groupSearch.addButton(self.rb_remote)
        self.bt_groupSearch.addButton(self.rb_hmmer)
        self.bt_groupSearch.addButton(self.rb_comLoc)
        self.bt_groupSearch.addButton(self.rb_comRem)

    def make_bgroup_binary_key(self):
        self.bt_groupKey = QButtonGroup()
        self.bt_groupKey.addButton(self.rb_btMax)
        self.bt_groupKey.addButton(self.rb_btSum)
        self.bt_groupKey.addButton(self.rb_btLen)

    def make_bgroup_binary_hit(self):
        self.bt_groupHit = QButtonGroup()
        self.bt_groupHit.addButton(self.rb_btID)
        self.bt_groupHit.addButton(self.rb_btCov)
        self.bt_groupHit.addButton(self.rb_btBit)
        self.bt_groupHit.addButton(self.rb_btEval)

    def get_search_options(self):
        searchMode = self.bt_groupSearch.checkedButton().text()
        if searchMode == "Local":
            seq_input = self.le_inBrowse.text()
            dia_db = self.le_sDiaBrowse.text()
            nr_cpu = self.le_sCPU.text()
            return searchMode, seq_input, dia_db, nr_cpu
        elif searchMode == "Remote":
            seq_input = self.le_inBrowse.text()
            db = self.le_sDB.text()
            entrz = self.le_sEntrz.text()
            rid = self.le_sRID.text()
            max_hits = self.le_sMaxHits.text()
            return searchMode, seq_input, db, entrz, rid, max_hits
        elif searchMode == "HMMER":
            hmm_input = self.le_inHmm.text()
            dia_db = self.le_sDiaBrowse.text()
            fasta_db = self.le_sFasBrowse.text()
            pfam_db = self.le_sPfamBrowse.text()
            return searchMode, hmm_input, dia_db, fasta_db, pfam_db
        elif searchMode == "Combi local":
            seq_input = self.le_inBrowse.text()
            dia_db = self.le_sDiaBrowse.text()
            nr_cpu = self.le_sCPU.text()
            hmm_input = self.le_inHmm.text()
            fasta_db = self.le_sFasBrowse.text()
            pfam_db = self.le_sPfamBrowse.text()
            return searchMode, seq_input, dia_db, nr_cpu, hmm_input, fasta_db, pfam_db
        elif searchMode == "Combi remote":
            seq_input = self.le_inBrowse.text()
            db = self.le_sDB.text()
            entrz = self.le_sEntrz.text()
            rid = self.le_sRID.text()
            max_hits = self.le_sMaxHits.text()
            hmm_input = self.le_inHmm.text()
            dia_db = self.le_sDiaBrowse.text()
            fasta_db = self.le_sFasBrowse.text()
            pfam_db = self.le_sPfamBrowse.text()
            return searchMode, seq_input, db, entrz, rid, max_hits, hmm_input, dia_db, \
                   fasta_db, pfam_db

    def get_filter_options(self):
        # Filtering options
        max_eval = self.le_fMaxEval.text()
        min_id = self.le_fMinId.text()
        minQcov = self.le_fQuCov.text()
        recom = self.ch_fRecom.isChecked()
        rec_file = self.le_flSave.text()
        return max_eval, min_id, minQcov, recom, rec_file

    def get_summary_table_options(self):
        # Summary Table options
        sum_table = self.ch_SumTab.isChecked()
        st_deli = self.le_stDeli.text()
        st_decimal = self.lb_stDecimal.text()
        st_sort = self.ch_stSort.isChecked()
        st_hide_head = self.ch_stHide.isChecked()
        st_output = self.le_stSave.text()
        return sum_table, st_deli, st_decimal, st_sort, st_hide_head, st_output

    def get_binary_table_options(self):
        # Binary table options
        bin_table = self.ch_BinaryTab.isChecked()
        bthide_head = self.ch_btHide.isChecked()
        key_func = self.bt_groupKey.checkedButton().text()
        hit_attr = self.bt_groupHit.checkedButton().text()
        bt_decimal = self.lb_btDeci.text()
        bt_output = self.le_btSave.text()
        return bin_table, bthide_head, key_func, hit_attr, bt_decimal, \
               bt_output

    def get_figure_options(self):
        # Figure options
        figure = self.ch_Figure.isChecked()
        fig_out = self.le_fSave.text()
        return figure, fig_out

    def hide_options(self):
        # Hide search options not needed for local search when program starts
        self.label_16.hide()
        self.le_inHmm.hide()
        self.label_18.hide()
        self.le_sDB.hide()
        self.label_19.hide()
        self.le_sEntrz.hide()
        self.label_20.hide()
        self.le_sRID.hide()
        self.label_32.hide()
        self.le_sFasBrowse.hide()
        self.pb_sFasBrowse.hide()
        self.label_33.hide()
        self.le_sPfamBrowse.hide()
        self.pb_sPfamBrowse.hide()
        self.label_57.hide()
        self.le_sMaxHits.hide()
        # Hide summary table options
        self.label_40.hide()
        self.le_stDeli.hide()
        self.label_43.hide()
        self.lb_stDecimal.hide()
        self.horizontalSlider_3.hide()
        self.ch_stSort.hide()
        self.ch_stHide.hide()
        self.label_45.hide()
        self.le_stSave.hide()
        self.pb_stSave.hide()
        # Hide Binary table options
        self.label_49.hide()
        self.le_btDeli.hide()
        self.ch_btHide.hide()
        self.label_51.hide()
        self.rb_btMax.hide()
        self.rb_btSum.hide()
        self.rb_btLen.hide()
        self.label_52.hide()
        self.rb_btID.hide()
        self.rb_btCov.hide()
        self.rb_btBit.hide()
        self.rb_btEval.hide()
        self.label_53.hide()
        self.lb_btDeci.hide()
        self.horizontalSlider_5.hide()
        self.label_54.hide()
        self.le_btSave.hide()
        self.pb_btSave.hide()
        # Hide figure options
        self.label_56.hide()
        self.le_fSave.hide()
        self.pb_fSave.hide()


def main():
    # Create an instance of QtWidgets.QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Create an instance of the class
    window = Ui()
    window.show()
    # Start the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
