from scrapy.commands import crawl
from scrapy.exceptions import UsageError


class Command(crawl.Command):
    """Custom command for easier running of broad crawls"""
    requires_project = True

    def syntax(self):
        return "[options] [url1 [url2 [url3 ...]"

    def short_desc(self):
        return "Crawl for keywords/harvesting"

    def add_options(self, parser):
        super().add_options(parser)

        parser.add_option("-j", "--javascript", action="store_true",
                          dest='javascript',
                          help="enables javascript crawling(requires splash)00")
        parser.add_option("-d", "--depth", metavar='DEPTH', action="store",
                          dest="depth",
                          default=0, type=int,
                          help="sets the crawl depth(1 for single page crawl)")
        parser.add_option('-u', "--url-file", metavar='URL_FILE',
                          action="store", type=str, dest="url_file",
                          help="sets the file with the urls, otherwise use the commandline args")

    def process_options(self, args, opts):
        super().process_options(args, opts)
        if opts.depth:
            # set the depth if unavailable
            self.settings.set('DEPTH_LIMIT', opts.depth, priority='cmdline')
        if opts.url_file:
            # raise error if args already specified
            if len(args) != 0:
                raise UsageError("can't use both url file and url arguments")
            self.settings.set('START_URLS_FILE', opts.url_file,
                              priority='cmdline')

    def run(self, args, opts):
        # make sure at leas one way of specifying urls is used
        if len(args) == 0 and not opts.url_file:
            raise UsageError(
                'must specify either command line urls or and url file')

        if len(args) != 0:
            # pass the urls via the settings if pass via arguments
            self.settings.set('START_URLS', args, priority='cmdline')
        # select either the js or the normal spider depending on the
        # command line arguments
        spider = 'barrelspider' if not opts.javascript else 'jsbarrelspider'
        super().run([spider], opts)  # pass is as the crawl argument
