# Standard Python libraries
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)
import os
import sys
import glob
import shutil
import tempfile

# https://pandas.pydata.org/
import pandas as pd

# https://github.com/usnistgov/DataModelDict
from DataModelDict import DataModelDict as DM

# iprPy imports
from .. import rootdir
from ..record import loaded as record_loaded
from ..tools import screen_input, aslist
from .prepare import prepare
from .runner import runner
from .settings import load_run_directory

class Database(object):
    """
    Class for handling different database styles in the same fashion.  The
    class defines the common methods and attributes, which are then uniquely
    implemented for each style.  The available styles are loaded from the
    iprPy.databases submodule.
    """
    
    def __init__(self, host):
        """
        Initializes a connection to a database.
        
        Parameters
        ----------
        style : str
            The database style.
        host : str
            The host name (path, url, etc.) for the database.
        """
        # Get module information for current class
        self_module = sys.modules[self.__module__]
        self.__mod_file = self_module.__file__
        self.__mod_name = self_module.__name__
        if self.__mod_name == 'iprPy.Database.Database':
            raise TypeError("Don't use Database itself, only use derived classes")
        
        # Set property values
        self.__host = host
    
    def __str__(self):
        """
        Returns
        -------
        str
            The string representation of the database.
        """
        return 'database style '  + self.style + ' at ' + self.host
    
    @property
    def style(self):
        """str: The database style"""
        pkgname = self.__mod_name.split('.')
        return pkgname[2]
    
    @property
    def host(self):
        """str: The database's host."""
        return self.__host
    
    def get_records(self, name=None, style=None, query=None, return_df=False,
                    **kwargs):
        """
        Produces a list of all matching records in the database.
        
        Parameters
        ----------
        name : str, optional
            The record name or id to limit the search by.
        style : str, optional
            The record style to limit the search by.
            
        Returns
        ------
        list of iprPy.Records
            All records from the database matching the given parameters.
        
        Raises
        ------
        AttributeError
            If get_records is not defined for database style.
        """
        raise AttributeError('get_records not defined for Database style')
    
    def get_record(self, name=None, style=None, query=None, **kwargs):
        """
        Returns a single matching record from the database.  Issues an error
        if multiple or no matching records are found.
        
        Parameters
        ----------
        name : str, optional
            The record name or id to limit the search by.
        style : str, optional
            The record style to limit the search by.
            
        Returns
        ------
        iprPy.Record
            The single record from the database matching the given parameters.
        
        Raises
        ------
        AttributeError
            If get_record is not defined for database style.
        """
        raise AttributeError('get_record not defined for Database style')
    
    def get_records_df(self, name=None, style=None, query=None, full=True,
                       flat=False, **kwargs):
        """
        Produces a pandas.DataFrame of all matching records in the database.
        
        Parameters
        ----------
        style : str
            The record style to collect records of.
        full : bool, optional
            Flag used by the calculation records.  A True value will include
            terms for both the calculation's input and results, while a value
            of False will only include input terms (Default is True).
        flat : bool, optional
            Flag affecting the format of the dictionary terms.  If True, the
            dictionary terms are limited to having only str, int, and float
            values, which is useful for comparisons.  If False, the term
            values can be of any data type, which is convenient for analysis.
            (Default is False).
        
        Returns
        ------
        pandas.DataFrame
            All records from the database of the given record style.
        
        Raises
        ------
        AttributeError
            If get_record is not defined for database style.
        """
        raise AttributeError('get_records_df not defined for Database style')
    
    def add_record(self, record=None, name=None, style=None, content=None):
        """
        Adds a new record to the database.  Will issue an error if a
        matching record already exists in the database.
        
        Parameters
        ----------
        record : iprPy.Record, optional
            The new record to add to the database.  If not given, then name,
            style and content are required.
        name : str, optional
            The name to assign to the new record.  Required if record is not
            given.
        style : str, optional
            The record style for the new record.  Required if record is not
            given.
        content : str, optional
            The xml content of the new record.  Required if record is not
            given.
            
        Returns
        ------
        iprPy.Record
            Either the given record or a record composed of the name, style,
            and content.
        
        Raises
        ------
        AttributeError
            If add_record is not defined for database style.
        """
        raise AttributeError('add_record not defined for Database style')
    
    def update_record(self, record=None, name=None, style=None, content=None):
        """
        Replaces an existing record with a new record of matching name and
        style, but new content.  Will issue an error if exactly one
        matching record is not found in the databse.
        
        Parameters
        ----------
        record : iprPy.Record, optional
            The record with new content to update in the database.  If not
            given, content is required along with name and/or style to
            uniquely define a record to update.
        name : str, optional
            The name to uniquely identify the record to update.
        style : str, optional
            The style of the record to update.
        content : str, optional
            The new xml content to use for the record.  Required if record is
            not given.
            
        Returns
        ------
        iprPy.Record
            Either the given record or a record composed of the name, style,
            and content.
        
        Raises
        ------
        AttributeError
            If update_record is not defined for database style.
        """
        raise AttributeError('update_record not defined for Database style')
    
    def delete_record(self, record=None, name=None, style=None):
        """
        Permanently deletes a record from the database.  Will issue an error
        if exactly one matching record is not found in the database.
        
        Parameters
        ----------
        record : iprPy.Record, optional
            The record to delete from the database.  If not given, name and/or
            style are needed to uniquely define the record to delete.
        name : str, optional
            The name of the record to delete.
        style : str, optional
            The style of the record to delete.
        
        Raises
        ------
        AttributeError
            If delete_record is not defined for database style.
        """
        raise AttributeError('delete_record not defined for Database style')
    
    def get_tar(self, record=None, name=None, style=None, raw=False):
        """
        Retrives the tar archive associated with a record in the database.
        Issues an error if exactly one matching record is not found in the
        database.
        
        Parameters
        ----------
        record : iprPy.Record, optional
            The record to retrive the associated tar archive for.
        name : str, optional
            .The name to use in uniquely identifying the record.
        style : str, optional
            .The style to use in uniquely identifying the record.
        raw : bool, optional
            If True, return the archive as raw binary content. If
            False, return as an open tarfile. (Default is False)
            
        Returns
        -------
        tarfile or str
            The tar archive as an open tarfile if raw=False, or as a binary
            str if raw=True.
        
        Raises
        ------
        AttributeError
            If get_tar is not defined for database style.
        """
        raise AttributeError('get_tar not defined for Database style')
    
    def add_tar(self, record=None, name=None, style=None, tar=None, root_dir=None):
        """
        Archives and stores a folder associated with a record.  Issues an
        error if exactly one matching record is not found in the database, or
        the associated record already has a tar archive.
        
        Parameters
        ----------
        database_info : mdcs.MDCS
            The MDCS class used for accessing the curator database.
        record : iprPy.Record, optional
            The record to associate the tar archive with.  If not given, then
            name and/or style necessary to uniquely identify the record are
            needed.
        name : str, optional
            .The name to use in uniquely identifying the record.
        style : str, optional
            .The style to use in uniquely identifying the record.
        tar : bytes, optional
            The bytes content of a tar file to save.  tar cannot be given
            with root_dir.
        root_dir : str, optional
            Specifies the root directory for finding the directory to archive.
            The directory to archive is at <root_dir>/<name>.  (Default is to
            set root_dir to the current working directory.)  tar cannot be given
            with root_dir.
        
        Raises
        ------
        ValueError
            If style and/or name content given with record or the record already
            has an archive.
        """
        raise AttributeError('add_tar not defined for Database style')
    
    def update_tar(self, record=None, name=None, style=None, tar=None, root_dir=None):
        """
        Replaces an existing tar archive for a record with a new one.  Issues
        an error if exactly one matching record is not found in the database.
        The record's name must match the name of the directory being archived.
        
        Parameters
        ----------
        record : iprPy.Record, optional
            The record to associate the tar archive with.  If not given, then 
            name and/or style necessary to uniquely identify the record are 
            needed.
        name : str, optional
            .The name to use in uniquely identifying the record.
        style : str, optional
            .The style to use in uniquely identifying the record.
        tar : bytes, optional
            The bytes content of a tar file to save.  tar cannot be given
            with root_dir.
        root_dir : str, optional
            Specifies the root directory for finding the directory to archive.
            The directory to archive is at <root_dir>/<name>.  (Default is to
            set root_dir to the current working directory.)  tar cannot be given
            with root_dir.
        
        Raises
        ------
        AttributeError
            If update_tar is not defined for database style.
        """
        raise AttributeError('update_tar not defined for Database style')
    
    def delete_tar(self, record=None, name=None, style=None):
        """
        Deletes a tar file from the database.  Issues an error if exactly one
        matching record is not found in the database.
        
        Parameters
        ----------
        record : iprPy.Record, optional
            The record associated with the tar archive to delete.  If not
            given, then name and/or style necessary to uniquely identify
            the record are needed.
        name : str, optional
            .The name to use in uniquely identifying the record.
        style : str, optional
            .The style to use in uniquely identifying the record.
        
        Raises
        ------
        AttributeError
            If delete_tar is not defined for database style.
        """
        raise AttributeError('delete_tar not defined for Database style')
    
    def build_refs(self, lib_directory=None, refresh=False):
        """
        Adds reference records from a library to a database.
        
        Parameters
        ----------
        lib_directory : str, optional
            The directory path for the library.  If not given, then it will use
            the iprPy/library directory.
        refresh : bool or list, optional
            If False (default) only new reference records are added.  If True,
            all existing reference records are refreshed by deleting the
            current ones in the database and uploading the references in
            lib_directory.  If a list is given, then only the reference
            record styles named in the list are refreshed.
        """
        
        # Set default lib_directory
        if lib_directory is None:
            lib_directory = os.path.join(os.path.dirname(rootdir), 'library')
        lib_directory = os.path.abspath(lib_directory)
        
        # Handle refresh options
        if refresh is False:
            refresh_list = []
        else:
            all_refs = []
            for path in glob.iglob(os.path.join(lib_directory, '*')):
                if os.path.isdir(path):
                    all_refs.append(os.path.basename(path))
            if refresh is True:
                refresh_list = all_refs
            else:
                refresh_list = aslist(refresh)
                for style in refresh_list:
                    assert style in all_refs, str(style) + ' is not a reference record style'
        
        # Delete records to be refreshed
        for style in refresh_list:
            self.destroy_records(style)
        
        # Loop over all record styles in lib_directory
        for dir in glob.iglob(os.path.join(lib_directory, '*')):
            if os.path.isdir(dir):
                record_style = os.path.basename(dir)
                
                # Loop over all records of one style
                for record_file in glob.iglob(os.path.join(dir, '*')):
                    if os.path.splitext(record_file)[1].lower() in ['.xml', '.json']:
                        record_name = os.path.splitext(os.path.basename(record_file))[0]
                        
                        # Add record if needed
                        try:
                            self.add_record(content=record_file, style=record_style,
                                             name=record_name)
                        except:
                            pass
                        
                        # Add a record's tar if needed
                        if os.path.isdir(os.path.splitext(record_file)[0]):
                            try:
                                self.add_tar(root_dir=dir, name=record_name)
                            except:
                                pass
    
    def check_records(self, record_style=None):
        """
        Counts and checks on the status of records in a database.
        
        Parameters
        ----------
        record_style : str, optional
            The record style to check on.  If not given, then the available record
            styles will be listed and the user prompted to pick one.
        """
        if record_style is None:
            record_style = self.select_record_style()
        
        if record_style is not None:
            # Display information about database records
            records = self.get_records_df(style=record_style, full=False, flat=True)
            print('In', self, ':')
            print('-', len(records), 'of style', record_style)
            sys.stdout.flush()
            if len(records) > 0 and 'calculation' in record_style:
                count = len(records[records.status == 'finished'])
                print(' -', count, 'are complete')
                sys.stdout.flush()
                
                count = len(records[records.status == 'not calculated'])
                print(' -', count, 'still to run')
                sys.stdout.flush()
                
                count = len(records[records.status == 'error'])
                print(' -', count, 'issued errors')
                sys.stdout.flush()
    
    def clean_records(self, run_directory=None, record_style=None, records=None):
        """
        Resets all records of a given style that issued errors. Useful if the
        errors are due to external conditions.
        
        Parameters
        ----------
        run_directory : str, optional
            The directory where the cleaned calculation instances are to be
            returned.
        record_style : str, optional
            The record style to clean.  If not given, then the available record
            styles will be listed and the user prompted to pick one.
        records : list, optional
            A list of iprPy.Record obejcts from the database to clean.  Allows
            the user full control on which records to reset.  Cannot be given
            with record_style.
        """
        
        if record_style is None and records is None:
            record_style = self.select_record_style()
            
        run_directory = load_run_directory(run_directory)
        
        if record_style is not None:
            if records is not None:
                raise ValueError('record_style and records cannot both be given')
            
            # Retrieve records with errors from self
            records = self.get_records(style=record_style, status='error')
        
        elif records is None:
            # Set empty list if record_style is still None and no records given
            records = []
        
        print(len(records), 'records to clean')
        
        # Loop over all error records
        for record in records:
            # Check if record has saved tar
            try:
                tar = self.get_tar(record=record)
            except:
                print('failed to extract', record_name, 'tar')
            else:
                # Copy tar back to run_directory
                try:
                    tar.extractall(run_directory)
                except:
                    print('failed to extract', record_name, 'tar')
                    tar.close()
                else:
                    # Delete database version of tar
                    tar.close()
                    try:
                        self.delete_tar(record=record)
                    except:
                        print('failed to delete', record_name, 'tar')
            
            # Remove error and status from stored record
            model = DM(record.content)
            model_root = list(model.keys())[0]
            del(model[model_root]['error'])
            model[model_root]['status'] = 'not calculated'
            self.update_record(record=record, content=model.xml())
        
        # Remove bid files
        for bidfile in glob.iglob(os.path.join(run_directory, '*', '*.bid')):
            os.remove(bidfile)
        
        # Remove results.json files
        for resultsfile in glob.iglob(os.path.join(run_directory, '*', 'results.json')):
            os.remove(resultsfile)
    
    def copy_records(self, dbase2, record_style=None, records=None, includetar=True, overwrite=False):
        """
        Copies records from one database to another.
        
        Parameters
        ----------
        dbase2 :  iprPy.Database
            The database to copy to.
        record_style : str, optional
            The record style to copy.  If record_style and records not
            given, then the available record styles will be listed and the
            user prompted to pick one.  Cannot be given with records.
        records : list, optional
            A list of iprPy.Record obejcts from the current database to copy
            to dbase2.  Allows the user full control on which records to
            copy/update.  Cannot be given with record_style.
        includetar : bool, optional
            If True, the tar archives will be copied along with the records.
            If False, only the records will be copied. (Default is True).
        overwrite : bool, optional
            If False (default) only new records and tars will be copied.
            If True, all existing content will be updated.
        """
        if record_style is None and records is None:
            # Prompt for record_style
            record_style = self.select_record_style()
        
        if record_style is not None:
            if records is not None:
                raise ValueError('record_style and records cannot both be given')
            
            # Retrieve records from self
            records = self.get_records(style=record_style)
        
        elif records is None:
            # Set empty list if record_style is still None and no records given
            records = []
        
        print(len(records), 'records to try to copy')
        
        record_count = 0
        tar_count = 0
        # Copy records
        for record in records:
            try:
                # Add new records
                dbase2.add_record(record=record)
                record_count += 1
            except:
                # Update existing records
                if overwrite:
                    dbase2.update_record(record=record)
                    record_count += 1
            
            # Copy archives
            if includetar:
                try:
                    # get tar if it exists
                    tar = self.get_tar(record=record, raw=True)
                except:
                    pass
                else:
                    try:
                        # Add new tar
                        dbase2.add_tar(record=record, tar=tar)
                        tar_count += 1
                    except:
                        # Update existing tar
                        if overwrite:
                            dbase2.update_tar(record=record, tar=tar)
                            tar_count += 1
        print(record_count, 'records added/updated')
        if includetar:
            print(tar_count, 'tars added/updated')
    
    def destroy_records(self, record_style=None):
        """
        Permanently deletes all records of a given style.
        
        Parameters
        ----------
        record_style : str, optional
            The record style to delete.  If not given, then the available record
            styles will be listed and the user prompted to pick one.
        """
        if record_style is None:
            record_style = self.select_record_style()
        
        records = self.get_records(style=record_style)
        print(len(records), 'records found for', record_style)
        if len(records) > 0:
            test = screen_input('Delete records? (must type yes):')
            if test == 'yes':
                count = 0
                for record in records:
                    try:
                        self.delete_tar(record=record)
                    except:
                        pass
                    try:
                        self.delete_record(record=record)
                        count += 1
                    except:
                        pass
                
                print(count, 'records successfully deleted')
    
    def select_record_style(self):
        """
        Console prompt for selecting a record_style
        """
        # Build list of calculation records
        styles = list(record_loaded.keys())
        
        # Ask for selection
        print('Select record_style:')
        for i, style in enumerate(styles):
            print(i+1, style)
        choice = screen_input(':')
        try:
            choice = int(choice)
        except:
            record_style = choice
        else:
            record_style = styles[choice-1]
        print()
        
        return record_style
    
    def get_parent_records(self, record=None, name=None, style=None):
        """
        Returns all records that are parents to the given one
        """
        if record is None:
            record = self.get_record(name=name, style=style)
        elif name is not None or style is not None:
            raise ValueError('record cannot be given with name/style')
        
        parents = []
        try:
            model = record.content.find('system-info')
        except:
            pass
        else:
            for load_file in record.content.find('system-info').finds('file'):
                d, b = os.path.split(os.path.normpath(load_file))
                if d != '':
                    pname = d
                else:
                    pname = os.path.splitext(b)[0]
                
                try:
                    parent = self.get_record(name=pname)
                except:
                    pass
                else:
                    parents.append(parent)
                    parents.extend(self.get_parent_records(parent))
        return parents
    
    def prepare(self, run_directory, calculation, **kwargs):
        prepare(self, run_directory, calculation, **kwargs)
    
    def runner(self, run_directory, orphan_directory=None, hold_directory=None):
        runner(self, run_directory, orphan_directory=None, hold_directory=None)